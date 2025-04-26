from flask import Flask, request, jsonify
import os
import sys
import re
import json
import logging
from pathlib import Path
from openai import OpenAI
import httpx
from prometheus_flask_exporter import PrometheusMetrics
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import gunicorn

# Configure logging
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Setup basic metrics for monitoring
metrics = PrometheusMetrics(app)

# Setup basic rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Initialize OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.warning("OPENAI_API_KEY environment variable is not set")

# Load system prompt once from file
SYSTEM_PROMPT_PATH = Path(os.environ.get("SYSTEM_PROMPT_PATH", "/app/system-prompt.txt"))
try:
    SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text()
    logger.info(f"Successfully loaded system prompt from {SYSTEM_PROMPT_PATH}")
except FileNotFoundError:
    # Fallback to looking in the current directory or parent directory
    fallback_paths = [Path("system-prompt.txt"), Path("../system-prompt.txt")]
    for path in fallback_paths:
        if path.exists():
            SYSTEM_PROMPT = path.read_text()
            logger.info(f"Successfully loaded system prompt from fallback path {path}")
            break
    else:
        SYSTEM_PROMPT = ""
        logger.error(f"System prompt file not found at {SYSTEM_PROMPT_PATH} or fallback locations")

# Custom httpx client without proxy
def create_client_without_proxy():
    """Create an OpenAI client that ignores proxy settings"""
    return OpenAI(
        api_key=api_key,
        http_client=httpx.Client(proxies=None)
    )

@app.route('/generate', methods=['POST'])
@limiter.limit("10 per minute")
def generate_commit_message():
    """Generate commit message(s) based on git diff"""
    if not api_key:
        logger.error("API request failed: OpenAI API key is not set")
        return jsonify({"error": "OpenAI API key is not set"}), 500

    data = request.get_json()
    diff = data.get("diff", "")

    if not diff:
        logger.warning("API request failed: No diff provided")
        return jsonify({"error": "No diff provided"}), 400

    try:
        client = create_client_without_proxy()
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate commit message(s) for this git diff:\n\n{diff}"}
            ]
        )

        raw_response = response.choices[0].message.content.strip()
        logger.debug(f"OpenAI raw response: {raw_response}")

        try:
            commit_messages = json.loads(raw_response)
        except json.JSONDecodeError:
            logger.error(f"Response is not valid JSON: {raw_response}")
            return jsonify({"error": "Response is not valid JSON", "raw": raw_response}), 500

        if not isinstance(commit_messages, list) or not all(isinstance(m, str) for m in commit_messages):
            logger.error(f"Response is not a list of strings: {raw_response}")
            return jsonify({"error": "Response is not a list of strings", "raw": raw_response}), 500

        warnings = []
        for msg in commit_messages:
            if not re.match(r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9/-]+\))?!?: .+', msg):
                warnings.append(f"Commit message does not fully match Conventional Commit format: {msg}")

        result = {"commits": commit_messages}
        if warnings:
            result["warning"] = warnings

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error generating commit message: {str(e)}")
        return jsonify({"error": f"Error generating commit message: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "openai_api_key_set": bool(api_key),
        "system_prompt_loaded": bool(SYSTEM_PROMPT)
    })

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logger.error(f"Server error: {e}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
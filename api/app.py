from flask import Flask, request, jsonify
import os
import sys
import re
import json
from pathlib import Path
from openai import OpenAI
import httpx

app = Flask(__name__)

# Initialize OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Warning: OPENAI_API_KEY environment variable is not set", file=sys.stderr)

# Load system prompt once from file
SYSTEM_PROMPT_PATH = Path("system-prompt.txt")
try:
    SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text()
except FileNotFoundError:
    SYSTEM_PROMPT = ""
    print("Error: system-prompt.txt not found", file=sys.stderr)

# Custom httpx client without proxy
def create_client_without_proxy():
    return OpenAI(
        api_key=api_key,
        http_client=httpx.Client(proxies=None)
    )

@app.route('/generate', methods=['POST'])
def generate_commit_message():
    if not api_key:
        return jsonify({"error": "OpenAI API key is not set"}), 500

    data = request.get_json()
    diff = data.get("diff", "")

    if not diff:
        return jsonify({"error": "No diff provided"}), 400

    try:
        client = create_client_without_proxy()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate commit message(s) for this git diff:\n\n{diff}"}
            ]
        )

        raw_response = response.choices[0].message.content.strip()

        try:
            commit_messages = json.loads(raw_response)
        except json.JSONDecodeError:
            return jsonify({"error": "Response is not valid JSON", "raw": raw_response}), 500

        if not isinstance(commit_messages, list) or not all(isinstance(m, str) for m in commit_messages):
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
        return jsonify({"error": f"Error generating commit message: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "openai_api_key_set": bool(api_key)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
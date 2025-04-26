FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Explicitly unset any proxy variables that might interfere with the OpenAI client
ENV http_proxy="" https_proxy="" HTTP_PROXY="" HTTPS_PROXY="" NO_PROXY="*"

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && apt-get clean

# Create a non-root user for security
RUN adduser --disabled-password --gecos "" appuser

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code with proper permissions
COPY --chown=appuser:appuser . .

# Switch to non-root user for security
USER appuser

EXPOSE 5000

# Health check - using shorter intervals for faster failure detection
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Use gunicorn for production, point to the correct module path
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "src.main:app"]
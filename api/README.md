# ccgen API

A simple API service that generates conventional commit messages from git diffs using OpenAI's GPT models.

## Quick Start

1. **Set up environment**

   ```bash
   # Copy the example environment file
   cp example.env .env

   # Add your OpenAI API key to the .env file
   echo "OPENAI_API_KEY=your_openai_api_key" >> .env
   ```

2. **Run with Docker**

   ```bash
   docker-compose up
   ```

3. **Generate a commit message**

   ```bash
   # Get the diff from your git repo
   git_diff=$(git diff)

   # Send to the API
   curl -X POST http://localhost:5000/generate \
     -H "Content-Type: application/json" \
     -d "{\"diff\": \"$git_diff\"}"
   ```

## API Endpoints

### Generate Commit Messages

```
POST /generate
```

**Request:**

```json
{
  "diff": "git diff content"
}
```

**Response:**

```json
{
  "commits": [
    "feat(api): add new endpoint for commit message generation",
    "fix(core): resolve issue with proxy settings"
  ]
}
```

### Health Check

```
GET /health
```

## Configuration

| Environment Variable | Description                    | Default |
| -------------------- | ------------------------------ | ------- |
| `OPENAI_API_KEY`     | Your OpenAI API key (required) | None    |
| `OPENAI_MODEL`       | OpenAI model to use            | gpt-4   |
| `LOG_LEVEL`          | Logging level                  | INFO    |

## Development

### Prerequisites

- Docker and Docker Compose
- OpenAI API key

### Running Tests

```bash
docker-compose -f docker-compose.test.yml up
```

### Production Deployment

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## CI/CD

This project includes automated testing and Docker image publishing through GitHub Actions when version tags are pushed.

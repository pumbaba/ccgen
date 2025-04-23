# ccgen API

A commit message generation API powered by OpenAI GPT models. This tool automatically generates meaningful commit messages from git diffs, saving developers time and improving repository documentation.

## Overview

The ccgen API uses advanced AI models to analyze git diffs and generate contextually appropriate commit messages. It supports various types of changes including:

- Feature additions
- Bug fixes
- Documentation updates
- Multiple file changes
- Breaking changes

## Docker Development Environment

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/)
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)
- OpenAI API key

### Development Setup

1. Clone the repository and navigate to the API directory:

   ```bash
   git clone https://github.com/yourusername/ccgen.git
   cd ccgen/api
   ```

2. Create a `.env` file in the api directory with your OpenAI API key:

   ```env
   OPENAI_API_KEY=your-openai-api-key
   ```

3. Start the development environment:

   ```bash
   docker-compose up -d
   ```

4. The API will be available at <http://localhost:5000>

5. To view logs:

   ```bash
   docker-compose logs -f
   ```

### API Endpoints

#### Health Check

```
GET /health
```

Returns status information about the API.

#### Generate Commit Messages

```
POST /generate
```

Accepts a JSON body containing a git diff and returns generated commit messages.

### API Usage Example

Send a POST request to the `/generate` endpoint with a JSON body containing a git diff:

```bash
curl -X POST \
  http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"diff": "your git diff content here"}'
```

The API will return a JSON response with generated commit messages:

```json
{
  "commits": [
    "feat: add new cool feature function",
    "Alternative: Implement new feature functionality"
  ]
}
```

## Testing

The project includes a test script that generates commit messages for various diff scenarios.

### Running Tests

1. Make sure the API server is running
2. Execute the test script:

   ```bash
   python test.py
   ```

The test script checks:

- API health status
- Commit message generation for various types of changes:
  - Simple feature additions
  - Bug fixes
  - Documentation updates
  - Multiple file changes
  - Breaking API changes

### Custom Tests

You can modify the `test_cases` list in `test.py` to add your own test cases with different types of diffs.

## Production Setup

For production deployment:

1. Pull the image from Docker Hub:

   ```bash
   export DOCKER_USERNAME=yourusername
   export TAG=latest
   export OPENAI_API_KEY=your-openai-api-key
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Publishing to Docker Hub

The project includes GitHub Actions workflow to automatically build and publish the Docker image when you:

1. Push to the main branch
2. Create a version tag (e.g., v1.0.0)

To enable this, add these secrets to your GitHub repository:

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password or access token
- `OPENAI_API_KEY`: Your OpenAI API key (for testing during CI)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT](LICENSE)

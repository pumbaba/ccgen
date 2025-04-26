# ccgen - Conventional Commit Generator

Generate high-quality, [conventional commit](https://www.conventionalcommits.org/) messages from git diffs using AI.

![Current Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## What is CCGen?

CCGen uses AI to analyze your code changes and automatically suggest well-formatted commit messages. It helps you:

- ✅ Save time writing commit messages
- ✅ Maintain consistent commit history
- ✅ Follow conventional commits standards
- ✅ Focus on coding, not on commit wording

## Quick Start

### Option 1: Use the API

```bash
# Clone the repository
git clone https://github.com/yourusername/ccgen.git
cd ccgen/api

# Setup with Docker
cp example.env .env
# Add your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" >> .env

# Start the service
docker-compose up -d
```

Generate a commit message:

```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" \
  -d "{\"diff\": \"$(git diff)\"}"
```

### Option 2: Use the CLI (Coming Soon!)

The command-line tool for easy integration into your Git workflow is under development.

## API Reference

| Endpoint    | Method | Description                            |
| ----------- | ------ | -------------------------------------- |
| `/generate` | POST   | Generate commit messages from git diff |
| `/health`   | GET    | Check API health status                |

See the [API README](api/README.md) for detailed instructions.

## Roadmap

- [x] API service for commit generation
- [ ] Command-line interface (CLI)
- [ ] Pre-commit hook integration
- [ ] VSCode extension

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

[MIT](LICENSE)

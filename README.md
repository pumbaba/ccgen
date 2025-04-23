# ccgen - Conventional Commit Generator

A tool for automatically generating high-quality commit messages from git diffs using AI. This project helps developers save time and maintain consistent commit history with minimal effort.

## Project Overview

ccgen uses OpenAI's GPT models to analyze git diffs and generate contextually appropriate commit messages that follow best practices. It supports all types of changes of the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification

## Project Components

This project consists of two main components:

- **API**: A Flask-based web service that uses OpenAI's GPT models to generate commit messages
- **CLI**: A command-line tool for interacting with the API directly from your git workflow

## Getting Started

### API Setup

The API service uses Docker for easy development and deployment. Navigate to the API directory and follow the setup instructions in the [API README](api/README.md)

### CLI Setup

**The CLI component is under development and will be available soon.**

## Usage

Once the API component is set up, you can generate commit messages through the API:

Send POST requests to the API with git diffs to get commit message suggestions:

```bash
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"diff": "your git diff content"}'
```

**The CLI component is under development and will be available soon.**

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT](LICENSE)

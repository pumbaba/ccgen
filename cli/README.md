# ccgen CLI

**The CLI component is under development and will be available soon.**

A command-line tool for generating commit messages using the ccgen API.

## Usage

```bash
# Set up the API URL and maximum diff size in the config file `~/.ccgen.json`
ccgen --api http://api.example.com
ccgen --max-diff 6000

# Generate a commit message for staged changes
# If no changes are staged, it will offer to stage all changes
# Displays the message and asks for confirmation before committing
ccgen
```

## Options

```txt
--api URL         API endpoint URL (overrides config)
--max-diff SIZE   Maximum diff size in characters (overrides config)
--help, -h        Show this help message
--version, -v     Show version information
```

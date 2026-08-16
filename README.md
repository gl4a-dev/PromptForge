# PromptForge

PromptForge is a Python library and CLI for generating LLM-ready representations of software projects.

It scans a software project, filters files according to the project's `.gitignore`, builds a representation of its directory structure, and combines the structure with the contents of its text files into a single prompt suitable for use with Large Language Models (LLMs).

## Features

* Scan software project directories.
* Respect `.gitignore` rules when selecting project files.
* Ignore the repository's internal `.git` directory.
* Generate a formatted representation of the project structure.
* Read and format text-based source files.
* Ignore binary files that cannot be decoded as UTF-8.
* Generate a single LLM-ready prompt containing the project structure and file contents.
* Use PromptForge directly from the command line.
* Use PromptForge components as a Python library.

## Installation

Clone the repository and install the project in a virtual environment:

```bash
git clone <repository-url>
cd PromptForge

python -m venv .venv
source .venv/bin/activate

pip install -e .
```

## CLI Usage

After installation, PromptForge can be executed using the `promptforge` command.

To generate a prompt for the current directory:

```bash
promptforge .
```

A project path can also be provided explicitly:

```bash
promptforge /path/to/project
```

Write directly to a UTF-8 file:

```bash
promptforge . --output prompt.md
```

or 

```bash
promptforge . -o prompt.md
```

To display the available CLI options:

```bash
promptforge --help
```

The generated prompt contains two main sections:

````text
# Project Structure

project
├── src
│   └── main.py
└── README.md

# File Contents

## src/main.py

```python
print("Hello, world!")
```

## README.md

...
````

Files ignored by the project's `.gitignore` are excluded from the generated representation. Binary files are also excluded from the file-content section.

## Using PromptForge as a Library

PromptForge can also be used programmatically from Python.

For example:

```python
from pathlib import Path

from promptforge.builders.prompt_builder import PromptBuilder
from promptforge.scanner.scanner import Scanner


scan_result = Scanner().scan(Path("."))

prompt = PromptBuilder().build(scan_result)

print(prompt)
````

The project is designed around independent components for scanning, filtering, tree construction, formatting, file reading, and prompt generation, allowing these components to be used independently when needed.

## Development

PromptForge uses `pytest` for testing.

Install the development environment and run the complete test suite with:

```bash
pytest
```

The test suite covers the project's core components as well as CLI integration.

## Version

Current version: **1.0.1**

## License

PromptForge is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# PromptForge

PromptForge is a Python library and CLI for generating LLM-ready representations of software projects.

It scans a software project, filters files according to configurable rules (including `.gitignore` and user-defined patterns), builds a representation of its directory structure, and combines the structure with the contents of its text files into a single prompt suitable for use with Large Language Models (LLMs).

## Features

- Scan software project directories.
- Automatically discover the Git repository root.
- Respect `.gitignore` rules by default.
- Optionally disable `.gitignore` filtering.
- Ignore additional files and directories using Git-style patterns.
- Ignore the repository's internal `.git` directory.
- Generate only the project tree or only file contents.
- Generate a formatted representation of the project structure.
- Read and format UTF-8 text source files.
- Ignore binary files that cannot be decoded as UTF-8.
- Generate a single LLM-ready prompt.
- Use PromptForge directly from the command line.
- Use PromptForge components as a Python library.

## Installation

Clone the repository and install the project in a virtual environment:

```bash
git clone <repository-url>
cd PromptForge

python -m venv .venv
source .venv/bin/activate

pip install -e .
```

Or install directly from Git:

```bash
python -m pip install "promptforge @ git+<repository-url>@<version>"
```

For example:

```bash
python -m pip install "promptforge @ git+https://github.com/gl4a-dev/PromptForge.git@v2.0.0"
```

## CLI Usage

After installation, PromptForge can be executed using the `promptforge` command.

Generate a prompt for the current directory:

```bash
promptforge .
```

Generate a prompt for another project:

```bash
promptforge /path/to/project
```

PromptForge automatically discovers the Git repository root, so it can also be executed from any subdirectory inside the repository.

### Writing to a File

Write the generated prompt directly to a UTF-8 file:

```bash
promptforge . --output prompt.md
```

or

```bash
promptforge . -o prompt.md
```

### Ignoring Files

By default, PromptForge respects the project's `.gitignore`.

You can disable this behavior:

```bash
promptforge . --no-gitignore
```

Additional files can be ignored using Git-style patterns:

```bash
promptforge . --ignore "*.csv"
```

Multiple patterns may be provided:

```bash
promptforge . \
    --ignore "*.csv" \
    --ignore "*.log"
```

or

```bash
promptforge . \
    -i "*.csv" \
    -i "*.log"
```

Ignored patterns are applied in addition to `.gitignore` (unless `--no-gitignore` is used).

### Output Modes

Generate only the project tree:

```bash
promptforge . --tree-only
```

Generate only the file contents:

```bash
promptforge . --content-only
```

These options are mutually exclusive.

### Complex Example

The following command:

- ignores the project's `.gitignore` file itself;
- ignores the `LICENSE` file;
- ignores every `__init__.py`;
- generates only file contents;
- writes the output directly to `prompt.md`.

```bash
promptforge . \
    -i ".gitignore" \
    -i "LICENSE" \
    -i "**/__init__.py" \
    --content-only \
    -o prompt.md
```

---

### Help

Display all available CLI options:

```bash
promptforge --help
```

## Generated Prompt

By default, PromptForge generates two sections:

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
`````

Using `--tree-only` generates only the **Project Structure** section.

Using `--content-only` generates only the **File Contents** section.

Files ignored by `.gitignore`, ignored through `--ignore`, or filtered by future CLI options are excluded from the generated output.

Binary files are omitted from the file-content section.

## Using PromptForge as a Library

PromptForge can also be used programmatically.

Example:

```python
from pathlib import Path

from promptforge.builders.prompt_builder import PromptBuilder
from promptforge.scanner.scanner import Scanner


scan_result = Scanner().scan(Path("."))

prompt = PromptBuilder().build(scan_result)

print(prompt)
```

The project is organized around independent components for:

* scanning;
* filtering;
* tree generation;
* tree formatting;
* file reading;
* prompt generation.

These components may be used independently when needed.

## Development

PromptForge uses `pytest`.

Run the complete test suite with:

```bash
pytest
```

The test suite covers:

* Scanner
* TreeBuilder
* TreeFormatter
* FileReader
* PromptBuilder
* FilterPipeline
* GitIgnoreFilter
* PatternFilter
* CLI integration

---

## Version

Current version: **2.0.0**

---

## License

PromptForge is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

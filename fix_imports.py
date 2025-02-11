#!/usr/bin/env python3
"""Fix imports and formatting issues in Python files."""

import re
from pathlib import Path


def fix_file(filepath: Path) -> None:
    """Fix imports and formatting in a single file."""
    with open(filepath) as f:
        content = f.read()

    # Remove unused imports
    content = re.sub(r"from datetime import datetime\n", "", content)
    content = re.sub(r"from typing import.*BinaryIO.*\n", "", content)
    content = re.sub(
        r"from typing import.*Optional.*\n", "from typing import Dict, List\n", content
    )
    content = re.sub(r"import os\n", "", content)

    # Fix line length issues
    content = content.replace(
        'raise ValueError("API token must be provided or set in GCORE_API_TOKEN environment variable")',
        'raise ValueError(\n        "API token must be provided or set in GCORE_API_TOKEN environment variable"\n    )',
    )

    with open(filepath, "w") as f:
        f.write(content)


def main():
    """Fix all Python files in the project."""
    project_root = Path(__file__).parent
    for filepath in project_root.rglob("*.py"):
        if filepath.name == "fix_imports.py":
            continue
        print(f"Fixing {filepath}")
        fix_file(filepath)


if __name__ == "__main__":
    main()

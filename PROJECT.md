# GEMINI.md

- All Python code must follow PEP 8 style.  
- Use 4 spaces for indentation.  

## Project Overview
`tablet-sync-epub` is a Python-based GUI utility designed to synchronize EPUB files between a reference directory and e-reader devices (such as KOReader or MoonReader on Android). It provides features to synchronize new books and "clean" read books from these devices by checking for a `V_` prefix on the reference files.

### Main Technologies
- **Python 3**
- **Tkinter**: Standard Python GUI toolkit.
- **ttkwidgets**: Used for the `CheckboxTreeview` component to allow selective file operations.
- **uv**: Recommended for fast dependency management and virtual environment creation.

## Building and Running

### Prerequisites
Ensure you have Python 3.10+ installed. It is recommended to use `uv`.
```bash
pip install uv
```

### Setup and Run
The project uses standard PEP 621 `pyproject.toml` metadata.

**Option 1: Using `uv` (Recommended)**
```bash
# Sync dependencies
uv sync

# Run the application
uv run tablet-sync-epub
```

**Option 2: Using standard `venv` and `pip`**
```bash
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # On Windows

# Install the package in editable mode
pip install -e .

# Run the application
tablet-sync-epub
# Alternatively: python -m tablet_sync_epub
```

## Development Conventions

- **GUI Architecture**: The application uses a single-window interface for managing device and reference paths.
- **File Naming & Synchronization Logic**:
  - `V_*.epub`: Files prefixed with `V_` in the reference path are treated as "read" and can be deleted from the target device using the "Clean read books" feature.
  - `.dir` directories: The application manages auxiliary directories (common in KOReader or MoonReader for metadata/bookmarks) that correspond to EPUB filenames.
- **Default Paths**:
  - Device path: `H:/Books`
  - Reference: `F:/Documents/eBook`

## Key Files
- `src/tablet_sync_epub/app.py`: Contains the entire GUI logic and file synchronization operations.
- `pyproject.toml`: Configuration and dependencies for the python package.
- `assets/`: Directory containing project image resources (`Foothill.jpg`, `Foothill.png`).
- `tests/`: Directory for project test cases.

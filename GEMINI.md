# GEMINI.md

- All Python code must follow PEP 8 style.  
- Use 4 spaces for indentation.  

## Project Overview
`tablet-sync-epub` is a Python-based GUI utility designed to synchronize EPUB files between a reference directory and e-reader devices (specifically Kindle with Duokan or Android with MoonReader). It provides features to synchronize new books and "clean" read books from these devices by checking for a `V_` prefix on the reference files.

### Main Technologies
- **Python 3**
- **Tkinter**: Standard Python GUI toolkit.
- **ttkwidgets**: Used for the `CheckboxTreeview` component to allow selective file operations.
- **PyInstaller**: Used for building a standalone executable (`main.exe`).

### Building the Executable
Build the executable:
   ```bash
   python -m PyInstaller src/main.spec
   ```
   The resulting executable will be found in the `dist/` directory after the build completes.

## Development Conventions

- **GUI Architecture**: The application uses a modular approach for creating windows and frames (`create_win`, `create_path_frame`, `create_button_frame`).
- **File Naming & Synchronization Logic**:
  - `V_*.epub`: Files prefixed with `V_` in the reference path are treated as "read" and can be deleted from the target device using the "Clean read books" feature.
  - `.dir` directories: The application manages auxiliary directories (common in Duokan for metadata/bookmarks) that correspond to EPUB filenames.
- **Default Paths**:
  - Kindle (Duokan): `H:/DK_Documents`
  - Android (MoonReader): `H:/Books`
  - Reference: `F:/Documents/eBook`

## Key Files
- `src/main.py`: Contains the entire GUI logic and file synchronization operations.
- `src/main.spec`: Configuration for PyInstaller to package the script into a Windows executable.
- `assets/`: Directory containing project image resources (`Foothill.jpg`, `Foothill.png`).
- `tests/`: Directory for project test cases.

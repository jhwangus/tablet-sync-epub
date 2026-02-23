# GEMINI.md

- All Python code must follow PEP 8 style.  
- Use 4 spaces for indentation.  

## Project Overview
`tablet-sync-epub` is a Python-based GUI utility designed to synchronize EPUB files between a reference directory and e-reader devices (specifically Kobo eReader or Android with MoonReader). It provides features to synchronize new books and "clean" read books from these devices by checking for a `V_` prefix on the reference files.

### Main Technologies
- **Python 3**
- **Tkinter**: Standard Python GUI toolkit.
- **ttkwidgets**: Used for the `CheckboxTreeview` component to allow selective file operations.
- **Briefcase (BeeWare)**: Used for building native installers (MSI on Windows).

## Building and Running

### Prerequisites
Ensure you have Python 3 installed. You will also need Briefcase.
```bash
pip install briefcase
```

### Running the Application
To run the app in development mode:
```bash
python -m briefcase dev
```

### Building the Native Installer
1. Create the application scaffold:
   ```bash
   python -m briefcase create
   ```
2. Build the application:
   ```bash
   python -m briefcase build
   ```
3. Package the application as an MSI:
   ```bash
   python -m briefcase package
   ```

## Development Conventions

- **GUI Architecture**: The application uses a modular approach for creating windows and frames (`create_win`, `create_path_frame`, `create_button_frame`).
- **File Naming & Synchronization Logic**:
  - `V_*.epub`: Files prefixed with `V_` in the reference path are treated as "read" and can be deleted from the target device using the "Clean read books" feature.
  - `.dir` directories: The application manages auxiliary directories (common in Kobo or MoonReader for metadata/bookmarks) that correspond to EPUB filenames.
- **Default Paths**:
  - Kobo eReader: `H:/Books`
  - Android (MoonReader): `H:/Books`
  - Reference: `F:/Documents/eBook`

## Key Files
- `src/tablet_sync_epub/app.py`: Contains the entire GUI logic and file synchronization operations.
- `pyproject.toml`: Configuration for Briefcase to package the app.
- `assets/`: Directory containing project image resources (`Foothill.jpg`, `Foothill.png`).
- `tests/`: Directory for project test cases.

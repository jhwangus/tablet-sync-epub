# Project Overview
`tablet-sync-epub` is a Python-based GUI utility designed to synchronize EPUB files between a reference directory and e-reader devices (specifically Kindle with Duokan or Android with MoonReader). It provides features to synchronize new books and "clean" read books from these devices by checking for a `V_` prefix on the reference files.

## Development Conventions

- **File Naming & Synchronization Logic**:
  - `V_*.epub`: Files prefixed with `V_` in the reference path are treated as "read" and can be deleted from the target device using the "Clean read books" feature.
  - `.dir` directories: The application manages auxiliary directories (common in Duokan for metadata/bookmarks) that correspond to EPUB filenames.
- **Default Paths**:
  - Kindle (Duokan): `H:/DK_Documents`
  - Android (MoonReader): `H:/Books`
  - Reference: `F:/Documents/eBook`


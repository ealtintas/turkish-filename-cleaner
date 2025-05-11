# Turkish Filename Cleaner

A Python script to clean and transform (normalize) filenames in a directory by applying a series of transformations. This tool helps you handle Turkish characters in filenames by converting them to ASCII, collapsing spaces, replacing spaces with underscores, converting to camelCase, and more.

## Features

- **Asciify**: Converts Turkish characters to ASCII equivalents (e.g., `ç` to `c`, `Ğ` to `G`).
- **Collapse Spaces**: Converts multiple spaces into a single space.
- **Replace Spaces with Underscores**: Optionally replace spaces with underscores.
- **Convert to camelCase**: Optionally convert filenames into camelCase after collapsing spaces.
- **Remove Non-ASCII Characters**: Optionally removes all non-ASCII characters like emojis.
- **Lowercase Filenames**: Optionally converts all filenames to lowercase.
- **Directory Processing**: Optionally applies the transformations to directory names as well.
- **Dry Run**: Preview the changes without renaming files.
- **File Extension Filtering**: Process only specific file extensions.
- **Verbose Output**: See detailed output of what will or won't change.

## Usage

```bash
python main.py [OPTIONS] [TARGET_DIR]
```

### Usage Examples

```bash
# Rename files normally (asciify only):
python main.py ~/my-folder

# Dry-run and show very detailed output:
python main.py ~/my-folder --dry-run -vv

# Collapse multiple spaces and replace spaces with underscores:
python main.py ~/my-folder --collapse-spaces --underscore

# Collapse spaces and convert to camelCase:
python main.py ~/my-folder --collapse-spaces --camelcase

# Only collapse spaces without asciify:
python main.py ~/my-folder --collapse-spaces --no-asciify

# Simulate renaming files and directories in `~/my-folder`, collapsing spaces, replacing them with underscores, converting them to lowercase, and only processing `.txt` and `.md` files:
python main.py ~/my-folder --dry-run --collapse-spaces --underscore --lowercase --process-dirs --extensions .txt .md
```

### Arguments:

- **TARGET_DIR**: The directory to scan and rename files.
- **-D, --dry-run**: Simulate renaming without actually changing the files.
- **-v, --verbose**: Increase verbosity level (e.g., use `-v` or `-vv`).
- **-s, --collapse-spaces**: Collapse multiple spaces into a single space.
- **-u, --underscore**: Replace spaces with underscores.
- **-c, --camelcase**: Convert filenames to camelCase after collapsing spaces.
- **-n, --no-asciify**: Disable the Turkish asciify transformation.
- **-a, --remove-non-ascii**: Remove all non-ASCII characters (like emojis).
- **-l, --lowercase**: Convert filenames to lowercase.
- **-d, --process-dirs**: Apply transformations to directory names too.
- **-e, --extensions**: Only process files with these extensions (e.g., `--extensions .jpg .txt`).
- **-v**: Displays more detailed output.
- **-vv**: Displays very detailed output, including skipping unchanged files and directories.

## Requirements

Only standard Python 3.x packages are used, so no extra installation is needed.


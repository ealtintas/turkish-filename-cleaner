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
❯ python src/main.py
usage: main.py [-h] [-D] [-v] [-s] [-u] [-n] [-a] [-l] [-d] [-e [EXTENSIONS ...]] [-S] [-U] [-c] target_dir
main.py: error: the following arguments are required: target_dir

❯ python src/main.py --help
usage: main.py [-h] [-D] [-v] [-s] [-u] [-n] [-a] [-l] [-d] [-e [EXTENSIONS ...]] [-S] [-U] [-c] target_dir

Clean and asciify Turkish filenames in a directory

positional arguments:
  target_dir            Target directory to scan and rename files

options:
  -h, --help            show this help message and exit
  -D, --dry-run         Simulate renaming without changing files
  -v, --verbose         Increase verbosity level (use -v, -vv)
  -s, --collapse-spaces
                        Collapse multiple spaces into a single space
  -u, --underscore      Replace spaces with underscores
  -n, --no-asciify      Disable Turkish asciify
  -a, --remove-non-ascii
                        Remove all non-ASCII characters (like emojis)
  -l, --lowercase       Lowercase all filenames
  -d, --process-dirs    Apply transformations to directory names too
  -e [EXTENSIONS ...], --extensions [EXTENSIONS ...]
                        Only process files with these extensions (e.g., --extensions .jpg .txt)
  -S, --safe-chars-only
                        Allow only safe chars (a-zA-Z0-9-_.), remove others
  -U, --replace-unsafe  Replace unsafe chars with underscore instead of removing
  -c, --camelcase       Convert filename into camelCase (after other transformations)
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

## Requirements

Only standard Python 3.x packages are used, so no extra installation is needed.


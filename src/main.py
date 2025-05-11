#!/usr/bin/env python
import os
import argparse
import logging
import re

# Turkish to ASCII mapping table
TURKISH_TO_ASCII_MAP = {
    'ç': 'c',
    'Ç': 'C',
    'ğ': 'g',
    'Ğ': 'G',
    'ö': 'o',
    'Ö': 'O',
    'ü': 'u',
    'Ü': 'U',
    'ı': 'i',
    'İ': 'I',
    'ş': 's',
    'Ş': 'S'
}

TURKISH_TRANSLATION_TABLE = str.maketrans(TURKISH_TO_ASCII_MAP)

# Safe characters that are allowed in filenames
SAFE_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_."
SAFE_CHARS_PATTERN = re.compile(rf'[^{re.escape(SAFE_CHARS)}]')

def asciify_filename(name: str) -> str:
    """Translate Turkish characters to ASCII."""
    return name.translate(TURKISH_TRANSLATION_TABLE)

def collapse_spaces(name: str) -> str:
    """Collapse multiple spaces into a single space."""
    return re.sub(r'\s+', ' ', name)

def replace_spaces_with_underscores(name: str) -> str:
    """Replace spaces with underscores."""
    return name.replace(' ', '_')

def remove_non_ascii(name: str) -> str:
    """Remove non-ASCII characters."""
    return name.encode('ascii', 'ignore').decode()

def lowercase_filename(name: str) -> str:
    """Convert filename to lowercase."""
    return name.lower()

def safe_chars_only(name: str, replace_unsafe: bool = False) -> str:
    """Remove or replace unsafe characters."""
    if replace_unsafe:
        return SAFE_CHARS_PATTERN.sub('_', name)
    else:
        return SAFE_CHARS_PATTERN.sub('', name)

def to_camel_case(name: str) -> str:
    """Convert filename (without extension) to camelCase."""
    if '.' in name:
        base, ext = name.rsplit('.', 1)
    else:
        base, ext = name, ''
    
    parts = re.split(r'[^A-Za-z0-9]+', base)
    if not parts:
        return name  # nothing to camelCase
    
    camel = parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])
    
    if ext:
        return f"{camel}.{ext}"
    return camel

def process_name(name: str, options) -> str:
    """Apply transformations according to options."""
    new_name = name
    if options.asciify:
        new_name = asciify_filename(new_name)
    if options.collapse_spaces:
        new_name = collapse_spaces(new_name)
    if options.underscore:
        new_name = replace_spaces_with_underscores(new_name)
    if options.remove_non_ascii:
        new_name = remove_non_ascii(new_name)
    if options.safe_chars_only:
        new_name = safe_chars_only(new_name, replace_unsafe=options.replace_unsafe)
    if options.lowercase:
        new_name = lowercase_filename(new_name)
    if options.camelcase:
        new_name = to_camel_case(new_name)
    return new_name

def should_process_file(filename: str, extensions: list) -> bool:
    """Check if file should be processed based on extension."""
    if not extensions:
        return True  # No filtering
    return any(filename.lower().endswith(ext.lower()) for ext in extensions)

def rename_file(original_path: str, new_path: str, dry_run: bool, verbosity: int):
    """Rename file and log actions."""
    if verbosity >= 1:
        print(f"{'[DRY-RUN]' if dry_run else '[RENAME]'} FILE {original_path} -> {new_path}")
    
    if not dry_run:
        try:
            os.rename(original_path, new_path)
        except Exception as e:
            logging.error(f"Failed to rename {original_path} to {new_path}: {e}")
    else:
        if verbosity >= 2:
            print(f"[SKIP] FILE {original_path} (no changes)")

def rename_files_in_directory(target_dir: str, dry_run: bool = False, verbosity: int = 1, options=None):
    """Walk through the directory and rename files (and optionally directories)."""
    for root, dirs, files in os.walk(target_dir, topdown=False):  # bottom-up to rename dirs after their contents
        # Process files
        for name in files:
            if not should_process_file(name, options.extensions):
                continue

            original_path = os.path.join(root, name)
            new_name = process_name(name, options)
            new_path = os.path.join(root, new_name)

            if name != new_name:
                rename_file(original_path, new_path, dry_run, verbosity)

        # Process directories if enabled
        if options.process_dirs:
            for name in dirs:
                original_dir_path = os.path.join(root, name)
                new_dir_name = process_name(name, options)
                new_dir_path = os.path.join(root, new_dir_name)

                if name != new_dir_name:
                    rename_file(original_dir_path, new_dir_path, dry_run, verbosity)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Clean and asciify Turkish filenames in a directory")
    parser.add_argument("target_dir", help="Target directory to scan and rename files")
    parser.add_argument("-D", "--dry-run", action="store_true", help="Simulate renaming without changing files")
    parser.add_argument("-v", "--verbose", action="count", default=1, help="Increase verbosity level (use -v, -vv)")
    parser.add_argument("-s", "--collapse-spaces", action="store_true", help="Collapse multiple spaces into a single space")
    parser.add_argument("-u", "--underscore", action="store_true", help="Replace spaces with underscores")
    parser.add_argument("-n", "--no-asciify", dest="asciify", action="store_false", help="Disable Turkish asciify")
    parser.add_argument("-a", "--remove-non-ascii", action="store_true", help="Remove all non-ASCII characters (like emojis)")
    parser.add_argument("-l", "--lowercase", action="store_true", help="Lowercase all filenames")
    parser.add_argument("-d", "--process-dirs", action="store_true", help="Apply transformations to directory names too")
    parser.add_argument("-e", "--extensions", nargs="*", help="Only process files with these extensions (e.g., --extensions .jpg .txt)")
    parser.add_argument("-S", "--safe-chars-only", action="store_true", help="Allow only safe chars (a-zA-Z0-9-_.), remove others")
    parser.add_argument("-U", "--replace-unsafe", action="store_true", help="Replace unsafe chars with underscore instead of removing")
    parser.add_argument("-c", "--camelcase", action="store_true", help="Convert filename into camelCase (after other transformations)")
    return parser.parse_args()


def main():
    """Main function to run the script."""
    args = parse_args()

    if args.verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not os.path.isdir(args.target_dir):
        logging.error(f"Provided path {args.target_dir} is not a directory or does not exist.")
        return

    rename_files_in_directory(args.target_dir, dry_run=args.dry_run, verbosity=args.verbose, options=args)


if __name__ == "__main__":
    main()

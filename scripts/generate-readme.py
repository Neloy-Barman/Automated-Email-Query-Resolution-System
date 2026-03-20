#!/usr/bin/env python3

"""
Script Run Command: - python -m scripts.generate-readme
"""

# ============================================================
#       README Generator: sections/ → README.md
# ============================================================
# - Reads all .md files from the sections/ folder
# - Merges them in order into a new README.md in root
# - Supports excluding specific files by name
# ============================================================

import os
import re

# ─────────────────────────────────────────────
#   CONFIGURATION (Edit here if needed)
# ─────────────────────────────────────────────

SECTIONS_FOLDER = "sections"
OUTPUT_FILE = "README.md"
SECTIONS_SEPARATOR = "\n\n---\n\n"
ADD_SEPARATOR = False

EXCLUDE_FILES = [
    "sections-to-complete.md",
]

# ✅ Fix paths: removes ../ prefix from all paths
FIX_ASSET_PATHS = True  # Set False to disable

# ─────────────────────────────────────────────


# Colors for terminal output
class Color:
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    BOLD = "\033[1m"
    NC = "\033[0m"  # No Color


def print_header():
    print(
        f"""
{Color.BLUE}{'=' * 50}{Color.NC}
{Color.BOLD}   README Generator: sections/ → README.md{Color.NC}
{Color.BLUE}{'=' * 50}{Color.NC}
    """
    )


def fix_asset_paths(content: str) -> str:
    """
    Removes all '../' occurrences from the content.

    ../assets/image.png  →  assets/image.png
    ../LICENSE           →  LICENSE
    ../assets/file.pdf   →  assets/file.pdf
    """

    # ✅ Simply remove every occurrence of ../
    content = content.replace("../", "")

    return content


def get_sorted_md_files(folder: str, exclude: list) -> list:
    """
    Get all .md files from the folder,
    sorted by filename (numeric prefix order),
    excluding specified files.
    """
    try:
        all_files = os.listdir(folder)
    except FileNotFoundError:
        print(f"{Color.RED}❌ Folder '{folder}' not found!{Color.NC}")
        exit(1)

    # Filter only .md files
    md_files = [f for f in all_files if f.endswith(".md")]

    # Exclude specified files
    filtered_files = [f for f in md_files if f not in exclude]

    # Sort by numeric prefix (01-, 02-, etc.)
    def sort_key(filename):
        match = re.match(r"^(\d+)", filename)
        return int(match.group(1)) if match else float("inf")

    sorted_files = sorted(filtered_files, key=sort_key)

    return sorted_files


def read_file(filepath: str) -> str:
    """Read content of a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def merge_sections(folder: str, files: list, add_separator: bool) -> str:
    """Merge all section files into one string."""
    merged_content = []

    for file in files:
        filepath = os.path.join(folder, file)
        content = read_file(filepath).strip()

        # ✅ Remove ../ from all paths before merging
        if FIX_ASSET_PATHS and content:
            content = fix_asset_paths(content)
            print(
                f"  {Color.GREEN}✅ Merged:{Color.NC} {Color.CYAN}{file}{Color.NC} {Color.YELLOW}(../ removed){Color.NC}"
            )
        elif content:
            print(f"  {Color.GREEN}✅ Merged:{Color.NC} {Color.CYAN}{file}{Color.NC}")
        else:
            print(f"  {Color.YELLOW}⚠️  Skipped (empty):{Color.NC} {file}")

        if content:
            merged_content.append(content)

    separator = SECTIONS_SEPARATOR if add_separator else "\n\n"
    return separator.join(merged_content)


def write_readme(output_file: str, content: str):
    """Write merged content to README.md."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
        f.write("\n")  # Newline at end of file


def print_summary(files: list, excluded: list, output: str):
    """Print a final summary."""
    print(
        f"""
{Color.BLUE}{'─' * 50}{Color.NC}
{Color.BOLD}📋 Summary:{Color.NC}

  {Color.GREEN}✅ Files Merged    : {len(files)}{Color.NC}
  {Color.YELLOW}⛔ Files Excluded  : {len(excluded)}{Color.NC}
  {Color.BLUE}📄 Output File     : {output}{Color.NC}
{Color.BLUE}{'─' * 50}{Color.NC}
    """
    )

    if excluded:
        print(f"{Color.YELLOW}  Excluded Files:{Color.NC}")
        for f in excluded:
            print(f"    {Color.RED}✗ {f}{Color.NC}")
        print()

    print(f"{Color.GREEN}{'=' * 50}{Color.NC}")
    print(f"{Color.BOLD}  ✅ README.md Generated Successfully!{Color.NC}")
    print(f"{Color.GREEN}{'=' * 50}{Color.NC}\n")


# ─────────────────────────────────────────────
#   MAIN
# ─────────────────────────────────────────────


def main():
    print_header()

    # Step 1: Get sorted and filtered .md files
    print(f"{Color.YELLOW}🔍 Scanning '{SECTIONS_FOLDER}' folder...{Color.NC}\n")
    files = get_sorted_md_files(SECTIONS_FOLDER, EXCLUDE_FILES)

    if not files:
        print(f"{Color.RED}❌ No .md files found in '{SECTIONS_FOLDER}'!{Color.NC}")
        exit(1)

    # Step 2: Show files to be merged
    print(f"{Color.BLUE}📂 Files to be merged (in order):{Color.NC}")
    for i, f in enumerate(files, 1):
        print(f"  {Color.CYAN}{i:02}. {f}{Color.NC}")
    print()

    # Step 3: Merge all sections
    print(f"{Color.YELLOW}🔀 Merging sections...{Color.NC}\n")
    merged = merge_sections(SECTIONS_FOLDER, files, ADD_SEPARATOR)

    # Step 4: Write to README.md
    print(f"\n{Color.YELLOW}💾 Writing to {OUTPUT_FILE}...{Color.NC}")
    write_readme(OUTPUT_FILE, merged)

    # Step 5: Print summary
    print_summary(files, EXCLUDE_FILES, OUTPUT_FILE)


if __name__ == "__main__":
    main()

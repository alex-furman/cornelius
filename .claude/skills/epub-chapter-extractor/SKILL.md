---
name: epub-chapter-extractor
description: Extract all chapters from an EPUB file into separate markdown files. Use when the user wants to split an EPUB into individual chapter files, extract EPUB chapters, or convert an ebook to separate markdown documents.
---

# EPUB Chapter Extractor

Extract each chapter from an EPUB file into its own markdown file.

## Instructions

From the repository root, run the bundled extraction script with `uv` (which
must be installed). Quote the input and output paths, including paths with spaces:

```bash
uv run --with ebooklib --with beautifulsoup4 --with html2text --with lxml python ".claude/skills/epub-chapter-extractor/extract_chapters.py" "/path/to/book.epub" "/path/to/output folder"
```

Omit the final output-directory argument to create a folder named after the EPUB
in the same directory. The script lives in this repository; a separate
`~/.claude/skills` installation is not required.

## Example

User: "Extract chapters from /Users/yourname/Books/mybook.epub"

```bash
uv run --with ebooklib --with beautifulsoup4 --with html2text --with lxml python ".claude/skills/epub-chapter-extractor/extract_chapters.py" "/Users/yourname/Books/mybook.epub"
```

Output files will be at `/Users/yourname/Books/mybook/`:
- `01_introduction.md`
- `02_chapter_one.md`
- etc.

After extraction, report the absolute output-directory path and files produced.
Opening a desktop folder is optional and only appropriate when requested: macOS
uses `open`, while a Linux desktop may provide `xdg-open`. Headless runtimes need
neither command.

## Output Format

Each chapter file contains:

```markdown
# Chapter Title

[Chapter content in markdown format]
```

Files are numbered for proper sorting: `01_`, `02_`, etc.

# KOReader Highlights to Obsidian Exporter

This Python script extracts KOReader highlights and notes (from synced sidecar files in Calibre) to Markdown files in your Obsidian vault.

## Disclaimer

Use at your own risk. **This script is highly personalized to my setup.** Adapt it for your Calibre columns, Markdown format, Obsidian frontmatter/properties/tags/metadata, and vault structure. Consider [KoHighlights](https://github.com/noembryo/KoHighlights) for a more general solution.

Thanks to Calibre, KOReader Sync, Obsidian, and Obsidian Web Clipper developers for their software and documentation.

## Prerequisites

- Python 3
- Calibre Library with synced KOReader sidecar files.
- Obsidian Vault
- KOReader Sync Calibre plugin.
- Custom Calibre Columns: for completion status, KOReader sidecar content in JSON.

## Usage

1.  Edit `db_path` and `export_path`.
2.  Sync KOReader annotations to Calibre.
3.  Verify custom column IDs match your setup. Ensure `#custom_column_8` contains KOReader sidecar JSON and `custom_column_9` contains the completion status.
4.  Run: `python koreader-export.py`.
5.  Markdown files will be in your `export_path`.

## Functionality

- Reads Calibre database.
- Finds finished books.
- Gets title and author.
- Creates safe filenames, skips books with existing exports.
- Retrieves and parses KOReader sidecar JSON from calibre custom column.
- Organizes by chapter (if available).
- Formats highlights and notes to liking in Markdown.
- Adds YAML frontmatter (author, alias, "unparsed" tag).
- Saves to Obsidian vault.

## Customization

- Adjust custom column IDs.
- Adapt parsing for different KOReader JSON structures.
- Modify YAML and Markdown formatting.

## TODO

- [ ] Fetch sidecar files from KOReader device mount point instead of relying on Calibre custom columns.
- [ ] Create a batch file for easier execution.
- [ ] Create separate config files.
- [ ] Make it into a Calibre plugin.

# Bibliography Maintenance Playbook

This repository contains tools to maintain the `panlab.bib` file, ensuring no duplicates are added and that published versions of papers replace their arXiv/preprint counterparts.

## Prerequisites

The scripts require Python 3 and `bibtexparser`.

```bash
pip install bibtexparser
```

## Workflows

### 1. Adding a Single Set of New Entries

If you have a list of new BibTeX entries (e.g., copied from Google Scholar or a journal website):

1.  **Paste** the entries into a file named `new.bib` in this directory.
2.  **Run** the helper script:
    ```bash
    ./add_bib.sh
    ```
    
**What happens:**
- `panlab.bib` is backed up to `panlab.bib.bak`.
- New entries are merged into `panlab.bib`.
- `new.bib` is deleted upon success.

### 2. Bulk Sync from Overleaf (Mac Only)

To sync references from all projects in your local Overleaf Dropbox folder:

1.  **Run** the sync script:
    ```bash
    python3 sync_overleaf.py
    ```
    
    *Optional arguments:*
    - `--dir`: Specify a different root directory to scan (default: `/Users/shaowupan/Library/CloudStorage/Dropbox/Apps/Overleaf`).
    - `--main`: Specify a different target bib file to update.

**What happens:**
- Scans `Dropbox/Apps/Overleaf` (recursive) for all `*.bib` files.
- Merges valid entries into `panlab.bib`.
- Skips files named `panlab.bib` to prevent self-merging.

## Deduplication Logic

The scripts use `update_bib.py` to handle merging. The logic is:

1.  **Normalization**: Titles are normalized (lowercase, alphanumeric only) to detect duplicates even with formatting differences.
2.  **Smart Replacement**:
    - If a **New** entry matches an **Existing** entry by title:
        - Checks if New is "Published" (has `journal`, `booktitle`, etc., and not "arXiv").
        - Checks if Old is "Preprint" (journal/publisher contains "arXiv" or "preprint").
        - **Action**: If a published version is found for an existing preprint, the **Old entry is REPLACED**.
    - Otherwise, duplicate is skipped (Existing entry is preserved).
3.  **Addition**: If no match is found, the New entry is **ADDED**.

## Files
- `panlab.bib`: The master bibliography file.
- `update_bib.py`: The core python logic for merging.
- `add_bib.sh`: Helper script for the single-file workflow.
- `sync_overleaf.py`: Helper script for the bulk sync workflow.

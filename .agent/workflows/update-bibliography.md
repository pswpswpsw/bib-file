---
description: How to update and maintain the panlab.bib bibliography
---

# Bibliography Update Workflow

## Quick Commands
// turbo-all
```bash
# Sync all Overleaf bib files into panlab.bib
python3 sync_overleaf.py

# Self-clean duplicates (both title and ID based)
python3 update_bib.py --main panlab.bib --out panlab.bib

# Add a single new.bib file
./add_bib.sh
```

## Key Lessons Learned

### 1. Deduplication Logic
- **Title-based**: Entries are matched by normalized titles (lowercase, alphanumeric only)
- **ID-based**: Entries with same BibTeX key are deduplicated (**case-insensitive** - `Tu2014` = `tu2014`)
- **Priority**: Published versions (journal/conference) are preferred over arXiv/preprints

### 2. Known Limitations
- `bibtexparser` skips non-standard entry types: `@software`, `@softmisc`, `@ieeetranbstctl`
- These entries must be added manually as `@misc` type

### 3. Citation Key Mapping
When user reports "missing citation" errors:
1. The entry likely EXISTS in `panlab.bib` under a DIFFERENT ID
2. Use this pattern to find the correct ID:
```bash
# Find the title of the missing key in Overleaf source
grep -A 5 "MISSING_KEY" /path/to/source.bib

# Search for that title in panlab.bib
grep -i "TITLE_SUBSTRING" panlab.bib

# Get the actual ID
grep -B 10 "TITLE" panlab.bib | grep "^@"
```

### 4. Fixing Papers with Wrong Citation Keys
Use sed to batch replace citation keys in a .tex file:
```bash
sed -i '' \
  -e 's/old_key1/new_key1/g' \
  -e 's/old_key2/new_key2/g' \
  /path/to/paper.tex
```

### 5. Source Locations
- **Main bib**: `/Users/shaowupan/Library/CloudStorage/Dropbox/Work_tools/bib-file/panlab.bib`
- **Overleaf bibs**: `/Users/shaowupan/Library/CloudStorage/Dropbox/Apps/Overleaf/**/*.bib`
- Note: Overleaf folder is OUTSIDE the bib-file workspace; use `run_command` to access

### 6. Git Workflow
After any changes to panlab.bib:
```bash
git add panlab.bib && git commit -m "Update bibliography" && git push
```

# Lab Reference Bibliography

This is the reference BibTeX bibliographic database for the Pan Lab.

## Quick Commands

```bash
# Sync all Overleaf bib files into panlab.bib
python3 sync_overleaf.py

# Self-clean duplicates (title and ID based, case-insensitive)
python3 update_bib.py --main panlab.bib --out panlab.bib

# Add entries from a single file
./add_bib.sh  # (expects new.bib in this folder)
```

## Guidelines

* Use this bib file for conference paper or journal paper
* Please report any corrections through PR. You should make sure there is no duplicate.
* Once you submit your paper, please add your bib entry through PR.

## Documentation

See [MAINTENANCE.md](MAINTENANCE.md) for detailed instructions and troubleshooting.

## Agent Workflows

This repo has a custom workflow at `.agent/workflows/update-bibliography.md`. Use `/update-bibliography` in the AI chat to trigger it.


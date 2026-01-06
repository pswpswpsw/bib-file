from update_bib import load_bib, normalize_title
import bibtexparser

dks_file = "/Users/shaowupan/Library/CloudStorage/Dropbox/Apps/Overleaf/[PAPER][NITHIN][Deep Koopman Sensing]/dks.bib"
main_file = "panlab.bib"

# Load panlab.bib
print("Loading panlab.bib...")
db = load_bib(main_file)
title_set = set()
for e in db.entries:
    if 'title' in e:
        norm = normalize_title(e['title'])
        if norm:
            title_set.add(norm)

print(f"panlab.bib has {len(db.entries)} entries, {len(title_set)} unique titles.")

# Load dks.bib
print(f"Loading {dks_file}...")
with open(dks_file, errors='ignore') as f:
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    dks_db = bibtexparser.load(f, parser=parser)

print(f"dks.bib has {len(dks_db.entries)} entries.")

# Find missing
missing = []
for e in dks_db.entries:
    if 'title' in e:
        norm = normalize_title(e['title'])
        if norm and norm not in title_set:
            missing.append((e.get('ID'), e.get('title')[:60]))

print(f"\nMissing from panlab.bib: {len(missing)}")
for m in missing[:20]:
    print(f"  - {m[0]}: {m[1]}")
if len(missing) > 20:
    print(f"  ... and {len(missing) - 20} more")

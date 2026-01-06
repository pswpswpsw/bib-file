from update_bib import load_bib, merge_db
import bibtexparser

main_file = "panlab.bib"
target_file = "/Users/shaowupan/Library/CloudStorage/Dropbox/Apps/Overleaf/FoamAgent/sn-bibliography.bib"

print(f"Loading {main_file}...")
original_db = load_bib(main_file)

print(f"Loading {target_file}...")
try:
    with open(target_file) as bibtex_file:
         parser = bibtexparser.bparser.BibTexParser(common_strings=True)
         new_db = bibtexparser.load(bibtex_file, parser=parser)
except Exception as e:
    print(f"FAILED to load {target_file}: {e}")
    exit(1)

print(f"New DB entries: {len(new_db.entries)}")

# Check if Jumper2021AlphaFold is in new_db
found = False
for e in new_db.entries:
    if e.get('ID') == 'Jumper2021AlphaFold':
        found = True
        print("Found Jumper2021AlphaFold in source parser.")
        print(f"Title: {e.get('title')}")
        break

if not found:
    print("CRITICAL: Jumper2021AlphaFold NOT found in parsed source file!")

# Try merge
added, replaced, skipped = merge_db(original_db, new_db)
print(f"Merge result: Added {added}, Replaced {replaced}, Skipped {skipped}")

from update_bib import load_bib, normalize_title
import bibtexparser
import glob
import os

missing_keys = [
    "brunton2015closed",
    "kalman1960filter", 
    "kalnay2003da",
    "holmes1996turbulence",
    "vlachas2018lstm",
    "koopman1931",
    "schmid2010dmd",
    "tu2014dmd",
    "jovanovic2014spdmd",
    "williams2015edmd",
    "lusch2018deep",
    "somasnhybridae",
    "adrian1994lse"
]

overleaf_dir = "/Users/shaowupan/Library/CloudStorage/Dropbox/Apps/Overleaf"
main_file = "panlab.bib"

# Load panlab.bib and index by normalized title
print("Loading panlab.bib...")
db = load_bib(main_file)
title_to_id = {}
for e in db.entries:
    if 'title' in e:
        norm = normalize_title(e['title'])
        if norm:
            title_to_id[norm] = e.get('ID')

# Find the original titles for missing keys from Overleaf
key_to_title = {}
print("Scanning Overleaf for original titles...")
bib_files = glob.glob(os.path.join(overleaf_dir, "**", "*.bib"), recursive=True)

for bf in bib_files:
    try:
        with open(bf, errors='ignore') as f:
            content = f.read()
            found_any = any(k in content for k in missing_keys)
            if not found_any:
                continue
            parser = bibtexparser.bparser.BibTexParser(common_strings=True)
            new_db = bibtexparser.loads(content, parser=parser)
            for e in new_db.entries:
                if e.get('ID') in missing_keys:
                    key_to_title[e.get('ID')] = e.get('title')
    except:
        pass

# Match and output
print("\n--- MAPPING RESULTS ---")
for key in missing_keys:
    if key in key_to_title:
        title = key_to_title[key]
        norm = normalize_title(title)
        if norm in title_to_id:
            correct_id = title_to_id[norm]
            print(f"{key} -> {correct_id}")
        else:
            print(f"{key} -> NOT_FOUND (Title: {title[:50]})")
    else:
        print(f"{key} -> NO_SOURCE_FOUND")

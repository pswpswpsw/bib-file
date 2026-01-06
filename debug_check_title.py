from update_bib import load_bib, normalize_title

main_file = "panlab.bib"
target_title = "Highly accurate protein structure prediction with AlphaFold"
target_norm = normalize_title(target_title)

print(f"Target normalized: {target_norm}")

db = load_bib(main_file)

found = False
for e in db.entries:
    if 'title' in e:
        norm = normalize_title(e['title'])
        if norm == target_norm:
            print(f"FOUND MATCH!")
            print(f"ID: {e.get('ID')}")
            print(f"Title: {e.get('title')}")
            found = True
            break
            
if not found:
    print("NOT FOUND in panlab.bib")


import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
import re
import argparse
import sys
from collections import defaultdict

def normalize_title(title):
    """Normalize title for comparison: lowercase, remove non-alphanumeric."""
    if not title:
        return ""
    # Remove LaTeX commands roughly
    title = re.sub(r'\\[a-zA-Z]+', '', title)
    # Remove braces
    title = title.replace('{', '').replace('}', '')
    # Lowercase and keep only alphanumeric
    return "".join(c.lower() for c in title if c.isalnum())

def is_published(entry):
    """Check if an entry looks like a published paper (not arxiv)."""
    journal = entry.get('journal', '').lower()
    publisher = entry.get('publisher', '').lower()
    
    if 'arxiv' in journal or 'arxiv' in publisher:
        return False
    if 'preprint' in journal or 'preprint' in publisher:
        return False
    
    # If it has a journal or booktitle and didn't trigger above, it's likely published
    if entry.get('journal') or entry.get('booktitle'):
        return True
        
    return False

def load_bib(file_path):
    print(f"Loading {file_path}...")
    with open(file_path) as bibtex_file:
        parser = BibTexParser(common_strings=True)
        db = bibtexparser.load(bibtex_file, parser=parser)
    return db

def merge_db(original_db, new_db):
    # Build a map of normalized title -> index in the original entries list
    title_map = {}
    for i, entry in enumerate(original_db.entries):
        if 'title' in entry:
            norm_title = normalize_title(entry['title'])
            if norm_title:
                title_map[norm_title] = i
                
    added_count = 0
    replaced_count = 0
    skipped_count = 0
    
    for new_entry in new_db.entries:
        if 'title' not in new_entry:
            continue
            
        norm_title = normalize_title(new_entry['title'])
        if not norm_title: 
            continue
            
        if norm_title in title_map:
            # Duplicate found
            original_index = title_map[norm_title]
            original_entry = original_db.entries[original_index]
            
            # Check if we should replace
            new_is_pub = is_published(new_entry)
            old_is_pub = is_published(original_entry)
            
            if new_is_pub and not old_is_pub:
               # print(f"Replacing ArXiv/Preprint with Published version: {new_entry['title'][:50]}...")
                original_db.entries[original_index] = new_entry
                replaced_count += 1
            else:
               # print(f"Skipping duplicate: {new_entry['title'][:50]}... (Existing is kept)")
                skipped_count += 1
        else:
            # New entry
           # print(f"Adding new entry: {new_entry['title'][:50]}...")
            original_db.entries.append(new_entry)
            title_map[norm_title] = len(original_db.entries) - 1
            added_count += 1
            
    return added_count, replaced_count, skipped_count

def save_bib(db, output_file):
    print(f"Writing to {output_file}...")
    writer = BibTexWriter()
    with open(output_file, 'w') as bibtex_file:
        bibtex_file.write(writer.write(db))

def deduplicate_db(db):
    """Deduplicate entries within a single DB."""
    # Build a map of normalized title -> list of indices
    title_map = defaultdict(list)
    for i, entry in enumerate(db.entries):
        if 'title' in entry:
            norm_title = normalize_title(entry['title'])
            if norm_title:
                title_map[norm_title].append(i)
                
    indices_to_remove = set()
    removed_count = 0
    
    for norm_title, indices in title_map.items():
        if len(indices) > 1:
            # We have duplicates. Decide which one to keep.
            # Strategy: Prefer Published > arXiv. If equal, prefer the one with more fields? Or just the first one?
            # Let's simple pick the "best" one and mark others for removal.
            
            best_index = -1
            best_is_pub = False
            
            # First pass: find the best one
            for idx in indices:
                entry = db.entries[idx]
                is_pub = is_published(entry)
                
                if best_index == -1:
                    best_index = idx
                    best_is_pub = is_pub
                else:
                    if is_pub and not best_is_pub:
                        best_index = idx
                        best_is_pub = True
                    # If both are pub or both not, we keep the first one encountered (stable) 
                    # OR we could check for field count/completeness.
            
            # Second pass: mark others for removal
            for idx in indices:
                if idx != best_index:
                    indices_to_remove.add(idx)
                    removed_count += 1
                    
    # Rebuild entries list excluding removed indices
    # Sort indices in descending order to pop safely? Or just build a new list
    new_entries = [entry for i, entry in enumerate(db.entries) if i not in indices_to_remove]
    db.entries = new_entries
    
    return removed_count

def deduplicate_db_by_id(db):
    """Deduplicate entries within a single DB based on BibTeX ID."""
    id_map = defaultdict(list)
    for i, entry in enumerate(db.entries):
        if 'ID' in entry:
            id_map[entry['ID']].append(i)
                
    indices_to_remove = set()
    removed_count = 0
    
    for eid, indices in id_map.items():
        if len(indices) > 1:
            # We have duplicate IDs.
            # Strategy: Prefer Published > arXiv. If equal, prefer the one with more fields.
            
            best_index = -1
            best_score = -1
            
            # Simple scoring function
            def score_entry(entry):
                score = 0
                if is_published(entry): score += 10
                score += len(entry.keys()) # More fields = better?
                return score
            
            # First pass: find the best one
            for idx in indices:
                entry = db.entries[idx]
                score = score_entry(entry)
                
                if best_index == -1 or score > best_score:
                    best_index = idx
                    best_score = score
            
            # Second pass: mark others for removal
            for idx in indices:
                if idx != best_index:
                    indices_to_remove.add(idx)
                    removed_count += 1
                    
    # Rebuild entries list excluding removed indices
    new_entries = [entry for i, entry in enumerate(db.entries) if i not in indices_to_remove]
    db.entries = new_entries
    
    return removed_count

def update_bib(original_file, new_file, output_file):
    if new_file:
        original_db = load_bib(original_file)
        new_db = load_bib(new_file)
        
        added, replaced, skipped = merge_db(original_db, new_db)
        
        print(f"\nSummary (Merge):")
        print(f"Original entries: {len(original_db.entries) - added}")
        print(f"Added: {added}")
        print(f"Replaced: {replaced}")
        print(f"Skipped (Duplicates): {skipped}")
    else:
        # If no new file, just load original for self-dedup
        original_db = load_bib(original_file)
        
    print("Running self-deduplication (Title match)...")
    removed_title = deduplicate_db(original_db)
    print(f"Removed {removed_title} internal duplicates (Title match).")

    print("Running self-deduplication (ID match)...")
    removed_id = deduplicate_db_by_id(original_db)
    print(f"Removed {removed_id} internal duplicates (ID match).")
    
    print(f"Total entries: {len(original_db.entries)}")
    
    save_bib(original_db, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update BibTeX file avoiding duplicates.')
    parser.add_argument('--main', default='panlab.bib', help='Main BibTeX file')
    parser.add_argument('--new', help='New entries BibTeX file (optional)')
    parser.add_argument('--out', default='panlab_updated.bib', help='Output file')
    
    args = parser.parse_args()
    
    try:
        update_bib(args.main, args.new, args.out)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

import os
import glob
from update_bib import load_bib, merge_db, save_bib
import shutil
import argparse

def sync_overleaf(main_file, overleaf_dir):
    # Load main DB
    original_db = load_bib(main_file)
    print(f"Initial entries: {len(original_db.entries)}")
    
    # Find all bib files
    search_pattern = os.path.join(overleaf_dir, "**", "*.bib")
    bib_files = glob.glob(search_pattern, recursive=True)
    
    total_added = 0
    total_replaced = 0
    total_skipped = 0
    processed_files = 0
    
    for bib_file in bib_files:
        # Avoid merging the main file into itself if it happens to be in the tree (unlikely given paths, but good safety)
        if os.path.abspath(bib_file) == os.path.abspath(main_file):
            continue
            
        # Avoid merging files named 'panlab.bib' likely to be duplicates
        if os.path.basename(bib_file) == "panlab.bib":
           # print(f"Skipping potential duplicate source: {bib_file}")
            continue
            
        try:
            # print(f"Processing {processed_files+1}/{len(bib_files)}: {bib_file}")
            new_db = load_bib(bib_file)
            added, replaced, skipped = merge_db(original_db, new_db)
            
            total_added += added
            total_replaced += replaced
            total_skipped += skipped
            processed_files += 1
        except Exception as e:
            print(f"Error processing {bib_file}: {e}")
            
    print(f"\nFinal Summary:")
    print(f"Files processed: {processed_files}")
    print(f"Total Added: {total_added}")
    print(f"Total Replaced: {total_replaced}")
    print(f"Total Skipped: {total_skipped}")
    print(f"Final Entry Count: {len(original_db.entries)}")
    
    # Save back
    # Create backup first
    shutil.copy(main_file, main_file + ".bak")
    save_bib(original_db, main_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sync Overleaf bib files.')
    parser.add_argument('--main', default='panlab.bib', help='Main BibTeX file')
    parser.add_argument('--dir', default='/Users/shaowupan/Library/CloudStorage/Dropbox/Apps/Overleaf', help='Overleaf directory')
    
    args = parser.parse_args()
    sync_overleaf(args.main, args.dir)

#!/bin/bash

# Check if new.bib exists
if [ ! -f "new.bib" ]; then
    echo "❌ Error: 'new.bib' not found!"
    echo "👉 Please create a file named 'new.bib' in this folder and paste your new entries there."
    exit 1
fi

echo "📦 Backing up panlab.bib to panlab.bib.bak..."
cp panlab.bib panlab.bib.bak

echo "🔄 Running update..."
python3 update_bib.py --main panlab.bib --new new.bib --out panlab.bib

if [ $? -eq 0 ]; then
    echo "✅ Successfully updated panlab.bib"
    rm new.bib
    echo "🗑️  Removed new.bib (ready for next time)"
else
    echo "❌ Update failed!"
    echo "Restoring backup..."
    mv panlab.bib.bak panlab.bib
    exit 1
fi

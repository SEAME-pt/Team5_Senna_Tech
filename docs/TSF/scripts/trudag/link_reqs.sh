#!/bin/bash

# Directories to process
DIRS=("assertions" "assumptions" "evidences" "expectations")
BASE_DIR="docs/TSF/reqs"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=== Starting Smart Requirement Linking ===${NC}"

create_links_from_file() {
    local file=$1
    local child_id=$2 

    # Dynamic search for any field matching related_*_id:
    # This captures related_expectation_id, related_assertion_id, related_item_id, etc.
    grep "^related_.*_id:" "$file" | while read -r line; do
        # Extract everything after the colon
        parents_raw=$(echo "$line" | cut -d':' -f2 | tr -d ' \r')

        if [ ! -z "$parents_raw" ]; then
            # Split by comma in case there are multiple parents
            IFS=',' read -ra ADDR <<< "$parents_raw"
            for parent in "${ADDR[@]}"; do
                # Trim whitespace
                parent=$(echo "$parent" | xargs)
                
                # Skip placeholder templates
                if [[ "$parent" == *"-XXX" ]]; then continue; fi
                if [ -z "$parent" ]; then continue; fi

                echo -n "   🔗 Linking $parent -> $child_id ... "
                
                # Check if link already exists in the .dotstop.dot database
                if grep -q "\"$parent\" -> \"$child_id\"" .dotstop.dot; then
                    # Link exists: Mark as REVIEWED/LINKED
                    trudag manage set-link "$parent" "$child_id" --status LINKED > /dev/null 2>&1
                    echo -e "${GREEN}[REVIEWED]${NC}"
                else
                    # Link is new: Create it
                    trudag manage create-link "$parent" "$child_id" > /dev/null 2>&1
                    if [ $? -eq 0 ]; then 
                        echo -e "${GREEN}[CREATED]${NC}"
                    else 
                        echo -e "${RED}[ERROR]${NC} (Check if $parent exists)"
                    fi
                fi
            done
        fi
    done
}

for dir in "${DIRS[@]}"; do
    TARGET_DIR="$BASE_DIR/$dir"
    if [ ! -d "$TARGET_DIR" ]; then continue; fi
    
    echo ""
    echo -e "📂 Checking files in: ${YELLOW}$TARGET_DIR${NC}"
    
    # Process each markdown file
    find "$TARGET_DIR" -type f -name "*.md" | while read -r file; do
        if [[ "$file" == *".tmp" ]]; then continue; fi
        
        filename=$(basename -- "$file")
        name_no_ext="${filename%.*}"
        
        # Current item ID is the filename
        full_id="$name_no_ext" 

        create_links_from_file "$file" "$full_id"
    done
done

echo ""
echo -e "${GREEN}=== Linking Completed Successfully! ===${NC}"
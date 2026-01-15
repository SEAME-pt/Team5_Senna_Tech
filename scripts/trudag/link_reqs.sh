#!/bin/bash

# Directories to process
DIRS=("assertions" "assumptions" "evidences" "expectations")
BASE_DIR="reqs"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "=== Starting Automatic Requirement Linking ==="

create_links_from_file() {
    local file=$1
    local child_id=$2 

    # 1. Link: Expectation (Parent) -> Assertion (Child)
    # Search for "related_expectation_id: VALUE1, VALUE2..."
    parents_exp=$(grep "^related_expectation_id:" "$file" | cut -d':' -f2 | tr -d ' \r')

    if [ ! -z "$parents_exp" ] && [ "$parents_exp" != "EXP-XXX" ]; then
        IFS=',' read -ra ADDR <<< "$parents_exp"
        for parent in "${ADDR[@]}"; do
            echo -n "   🔗 Linking $parent -> $child_id ... "
            if grep -q "\"$parent\" -> \"$child_id\"" .dotstop.dot; then
                echo -e "${YELLOW}[KEPT]${NC}"
            else
                trudag manage create-link "$parent" "$child_id" > /dev/null 2>&1
                if [ $? -eq 0 ]; then 
                    echo -e "${GREEN}[CREATED]${NC}"
                else 
                    echo -e "${RED}[ERROR] (Check if $parent exists)${NC}"
                fi
            fi
        done
    fi

    # 2. Link: Assertion (Parent) -> Evidence/Assumption (Child)
    # Search for "related_item_id: VALUE1, VALUE2..."
    parents_ast=$(grep "^related_item_id:" "$file" | cut -d':' -f2 | tr -d ' \r')

    if [ ! -z "$parents_ast" ] && [ "$parents_ast" != "AST-XXX" ]; then
        IFS=',' read -ra ADDR <<< "$parents_ast"
        for parent in "${ADDR[@]}"; do
            echo -n "   🔗 Linking $parent -> $child_id ... "
            if grep -q "\"$parent\" -> \"$child_id\"" .dotstop.dot; then
                echo -e "${YELLOW}[KEPT]${NC}"
            else
                trudag manage create-link "$parent" "$child_id" > /dev/null 2>&1
                if [ $? -eq 0 ]; then 
                    echo -e "${GREEN}[CREATED]${NC}"
                else 
                    echo -e "${RED}[ERROR] (Check if $parent exists)${NC}"
                fi
            fi
        done
    fi
}

for dir in "${DIRS[@]}"; do
    TARGET_DIR="$BASE_DIR/$dir"
    if [ ! -d "$TARGET_DIR" ]; then continue; fi
    
    echo ""
    echo -e "📂 Checking links in: ${GREEN}$TARGET_DIR${NC}"
    
    find "$TARGET_DIR" -type f -name "*.md" | while read -r file; do
        if [[ "$file" == *".tmp" ]]; then continue; fi
        
        filename=$(basename -- "$file")
        name_no_ext="${filename%.*}"
        
        # Item ID is the filename (e.g., AST-201)
        full_id="$name_no_ext" 

        create_links_from_file "$file" "$full_id"
    done
done

echo ""
echo -e "${GREEN}=== Linking Completed! ===${NC}"

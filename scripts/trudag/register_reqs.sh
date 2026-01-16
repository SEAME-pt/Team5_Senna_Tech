#!/bin/bash

# Directories to process
DIRS=("assertions" "assumptions" "evidences" "expectations")
BASE_DIR="reqs"

# Output colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "=== Starting Secure Registration in Trudag ==="

# === STEP 0: DATABASE INITIALIZATION ===
if [ ! -f ".dotstop.dot" ]; then
    echo -e "${YELLOW}[WARN] Database (.dotstop.dot) not found. Initializing new database...${NC}"
    trudag init
    echo -e "${GREEN}[OK] Database initialized.${NC}"
else
    read -p "Do you want to clear and rebuild the database (.dotstop.dot)? [y/N] " response
    if [[ "$response" =~ ^[yY]$ ]]; then
        echo -e "🧹 Clearing old database..."
        rm -f .dotstop.dot
        trudag init
        echo -e "${GREEN}[OK] Database cleared and re-initialized.${NC}"
    else
        echo -e "⚠️  Keeping current database. New items will be added/updated."
    fi
fi

validate_file() {
    local file=$1
    local content=$(cat "$file")

    # 1. Check Normative
    if ! grep -q "normative: true" "$file"; then
        echo -e "${RED}[ERROR] $file missing 'normative: true'.${NC}"
        return 1
    fi

    # 2. Check for empty Score (Causes Trudag crash)
    if grep -q "^score:[[:space:]]*$" "$file"; then
        echo -e "${RED}[ERROR] $file contains empty 'score:' field. Remove it or set a value.${NC}"
        return 1
    fi

    # 3. Check for empty ID
    if grep -q "^id:[[:space:]]*$" "$file"; then
        echo -e "${RED}[ERROR] $file contains empty 'id:' field.${NC}"
        return 1
    fi

    return 0
}

for dir in "${DIRS[@]}"; do
    TARGET_DIR="$BASE_DIR/$dir"

    if [ ! -d "$TARGET_DIR" ]; then
        echo "Folder $TARGET_DIR not found, skipping..."
        continue
    fi

    echo ""
    echo -e "📂 Processing: ${YELLOW}$TARGET_DIR${NC} (recursive)"

    # Use find to search recursively and handle filenames with spaces correctly
    find "$TARGET_DIR" -type f -name "*.md" | while read -r file; do
        # Ignore temporary files
        if [[ "$file" == *".tmp" ]]; then continue; fi

        # === STAGE 1: VALIDATION ===
        if ! validate_file "$file"; then
            echo -e "${RED}Aborting process due to validation error in $file.${NC}"
            # The exit here leaves the subshell of the pipe, not the parent script, but serves to alert
            exit 1
        fi

        # === STAGE 2: EXTRACTION AND HASH VERIFICATION ===
        filename=$(basename -- "$file")
        dirname=$(dirname -- "$file")
        name_no_ext="${filename%.*}"

        # Extract prefix and ID for Trudag
        id_suffix="${name_no_ext##*-}"
        prefix="${name_no_ext%-*}"

        echo -n "   -> Item $name_no_ext: "

        # Calculate hash of current file (content only, ignoring leading/trailing whitespace)
        current_sha=$(sha256sum "$file" | awk '{print $1}')
        # Search hash in .dotstop.dot database
        stored_sha=$(grep "\"$name_no_ext\"" .dotstop.dot | grep -o 'sha="[^"].*"' | cut -d'"' -f2)

        if [ "$current_sha" == "$stored_sha" ]; then
            echo -e "${YELLOW}[NO CHANGES]${NC}"
            continue
        fi

        # === STAGE 3: REGISTRATION OR UPDATE ===
        if [ -z "$stored_sha" ]; then
            echo -n "Registering NEW item... "
            # Security process for NEW items only
            cp "$file" "$file.tmp"
            rm "$file"
            error_msg=$(trudag manage create-item "$prefix" "$id_suffix" "$dirname" 2>&1)
            res=$?
            mv "$file.tmp" "$file"
        else
            echo -n "Synchronizing CHANGES... "
            # Update only the hash in the database without touching the physical file
            error_msg=$(trudag manage set-item "$name_no_ext" 2>&1)
            res=$?
        fi

        if [ $res -eq 0 ]; then
            echo -e "${GREEN}[OK]${NC}"
        else
            echo -e "${RED}[FAILED]${NC}"
            echo -e "      Error: $error_msg"
        fi
    done
done

# === STEP 4: AUTOMATIC LINKING ===
./scripts/trudag/link_reqs.sh

echo ""

echo -e "${GREEN}=== Registration Completed Successfully! ===${NC}"

echo -e "${CYAN}Next Steps:${NC}"

echo -e "  1. Score Command:    ${YELLOW}trudag score${NC}"
echo -e "  2. Graph Command:    ${YELLOW}trudag plot${NC}"
echo -e "  3. Visualize Site Command:   ${YELLOW}./scripts/trudag/preview_site.sh${NC}"

echo ""

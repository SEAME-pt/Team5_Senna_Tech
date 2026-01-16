#!/bin/bash
set -e

# Directory containing the generated docs
DOCS_DIR="docs/trustable"

# ANSI Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}[INFO] Starting Markdown attribute fix in $DOCS_DIR...${NC}"

# Find all .md files in the directory
find "$DOCS_DIR" -type f -name "*.md" | while read -r file; do
    # Check if the file contains the problematic tag
    if grep -q "{: .expanded-item-element }" "$file"; then
        echo -n "   Fixing $file... "
        
        # Use sed to merge attributes.
        # Logic:
        # 1. Read the file into memory/buffer.
        # 2. Look for the pattern: 
        #    Line A: ... }
        #    (Empty lines)
        #    Line B: {: .expanded-item-element }
        # 3. Append .expanded-item-element to Line A (inside the closing brace) and delete Line B.
        
        # Implementation via Perl (more robust regex than sed for multiline):
        # s/(\}[ \t]*)\n\s*\{: \.expanded-item-element \}/ .expanded-item-element \1/g
        
        perl -0777 -i -pe 's/(\}[ \t]*)\n\n\s*\{: \.expanded-item-element \}/ .expanded-item-element \1/g' "$file"
        
        # Also catch single newline case just to be safe
        perl -0777 -i -pe 's/(\}[ \t]*)\n\s*\{: \.expanded-item-element \}/ .expanded-item-element \1/g' "$file"

        echo -e "${GREEN}[DONE]${NC}"
    fi
done

echo -e "${GREEN}[SUCCESS] All files processed.${NC}"

#!/bin/bash
set -e

# ANSI Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Find project root
PROJECT_ROOT=$(git rev-parse --show-toplevel)
cd "$PROJECT_ROOT"

echo -e "${CYAN}[INFO] Preparing Safety Documentation Site...${NC}"

# 1. Publish (Generate Markdown from Trudag DB)
echo -e "${YELLOW}-> Running trudag publish...${NC}"
trudag publish

# 2. Fix Markdown (Apply visual patches)
echo -e "${YELLOW}-> Fixing Markdown attributes...${NC}"
bash scripts/trudag/fix_markdown_attributes.sh

# 3. Serve (Start Web Server)
echo -e "${GREEN}[READY] Starting local server...${NC}"
echo -e "Press Ctrl+C to stop."
echo ""
mkdocs serve -f docs/trustable/mkdocs_trustable.yml

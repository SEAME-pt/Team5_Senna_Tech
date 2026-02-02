#!/bin/bash
set -e

# ANSI Color Codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
REQUIRED_PYTHON="python3.12"
PROJECT_ROOT=$(git rev-parse --show-toplevel)
VENV_PATH="$PROJECT_ROOT/venv"
DEPS_FILE="$PROJECT_ROOT/docs/TSF/scripts/trudag/trudag_aux_dependences.txt"

# --- PROGRESS BAR FUNCTION ---
progress_bar() {
    local pid=$1
    local width=20
    local i=0
    local direction=1
    local messages=("Downloading packages..." "Scanning requirements..." "Almost there..." "Optimizing workspace..." "Brewing coffee..." "Checking versions...")
    local msg_idx=0
    local counter=0
    
    # Hide cursor
    tput civis
    
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        # Change message every 2 seconds (20 * 0.1s)
        if [ $counter -eq 20 ]; then
            msg_idx=$(( (msg_idx + 1) % ${#messages[@]} ))
            counter=0
        fi
        
        printf "\r["
        
        # Print spaces before
        for ((j=0; j<i; j++)); do printf " "; done
        
        # Print the moving block
        printf "%s" "======"
        
        # Print spaces after
        for ((j=i+6; j<width; j++)); do printf " "; done
        
        printf "] %-30s" "${messages[$msg_idx]}"
        
        # Update position
        if [ $i -ge $((width - 6)) ]; then direction=-1; fi
        if [ $i -le 0 ]; then direction=1; fi
        i=$((i + direction))
        
        counter=$((counter + 1))
        sleep 0.1
    done
    
    # Show cursor again and clear line
    tput cnorm
    printf "\r%-60s\n" " "
}

# --- INTERACTIVE PROMPT ---
FORCE_INSTALL_FLAG=""
echo -e "${CYAN}[PROMPT] Do you want to force a clean reinstall of all dependencies? (y/N)${NC}"
read -p "> " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}[INFO] Force reinstall selected. Please wait...${NC}"
    FORCE_INSTALL_FLAG="--force-reinstall"
else
    echo -e "${CYAN}[INFO] Normal check selected.${NC}"
fi

# --- VENV CHECK ---
echo -e "${CYAN}[INFO] Checking virtual environment at $VENV_PATH...${NC}"
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}[WARN] Virtual environment not found. Creating one with $REQUIRED_PYTHON...${NC}"
    if command -v $REQUIRED_PYTHON >/dev/null 2>&1; then
        $REQUIRED_PYTHON -m venv "$VENV_PATH"
        echo -e "${GREEN}[OK] venv created.${NC}"
    else
        echo -e "${RED}[ERROR] $REQUIRED_PYTHON not found.${NC}"
        exit 1
    fi
fi

echo -e "${CYAN}[INFO] Activating virtual environment...${NC}"
source "$VENV_PATH/bin/activate"

# Python Version Check
INSTALLED_PYTHON_VER=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [ "$INSTALLED_PYTHON_VER" != "3.12" ]; then
    echo -e "${YELLOW}[WARN] Existing venv uses Python $INSTALLED_PYTHON_VER (Expected: 3.12).${NC}"
fi

# --- PIP INSTALL WITH PROGRESS BAR ---
echo -e "${CYAN}[INFO] Installing/Updating dependencies...${NC}"

if [ -f "$DEPS_FILE" ]; then
    # Run pip in background
    pip install -q $FORCE_INSTALL_FLAG -r "$DEPS_FILE" > /tmp/pip_install.log 2>&1 &
    PID=$!
    
    # Run animation
    progress_bar $PID
    
    # Wait for completion status
    wait $PID
    EXIT_STATUS=$?
    
    if [ $EXIT_STATUS -eq 0 ]; then
        echo -e "${GREEN}[OK] Dependencies installed successfully!${NC}"
    else
        echo -e "${RED}[ERROR] Installation failed. Check /tmp/pip_install.log for details.${NC}"
        cat /tmp/pip_install.log
        exit 1
    fi
else
    echo -e "${RED}[ERROR] $DEPS_FILE not found.${NC}"
    exit 1
fi

# --- VERIFICATION ---
echo -e "${GREEN}[CHECK] Verifying tools:${NC}"
trudag --version
mkdocs --version

echo ""
echo -e "${GREEN}[DONE] Environment is ready! Run 'source venv/bin/activate' to start.${NC}"
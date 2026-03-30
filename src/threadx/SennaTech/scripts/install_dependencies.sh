#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_msg() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        VERSION=$VERSION_ID
    else
        print_error "Cannot detect OS"
        exit 1
    fi
    
    print_msg "Detected OS: $OS $VERSION"
    
    # Check if Debian-based
    case "$OS" in
        ubuntu|debian|linuxmint|pop)
            print_success "Debian-based system detected"
            ;;
        *)
            print_error "This script only supports Debian-based systems (Ubuntu, Debian, Linux Mint, Pop!_OS)"
            print_msg "Please install dependencies manually:"
            echo "  - CMake"
            echo "  - ARM GCC toolchain (arm-none-eabi-gcc)"
            echo "  - ST-Link tools (stlink-tools)"
            exit 1
            ;;
    esac
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install dependencies on Ubuntu/Debian
install_ubuntu_debian() {
    print_msg "Installing dependencies for Ubuntu/Debian..."
    
    # Update package list
    print_msg "Updating package list..."
    sudo apt-get update || { print_error "Failed to update package list"; exit 1; }
    
    # Install CMake
    if ! command_exists cmake; then
        print_msg "Installing CMake..."
        sudo apt-get install -y cmake || { print_error "Failed to install CMake"; exit 1; }
        print_success "CMake installed"
    else
        print_success "CMake already installed ($(cmake --version | head -n1))"
    fi
    
    # Install ARM GCC toolchain
    if ! command_exists arm-none-eabi-gcc; then
        print_msg "Installing ARM GCC toolchain..."
        sudo apt-get install -y gcc-arm-none-eabi binutils-arm-none-eabi || {
            print_error "Failed to install ARM GCC toolchain"
            exit 1
        }
        print_success "ARM GCC toolchain installed"
    else
        print_success "ARM GCC toolchain already installed ($(arm-none-eabi-gcc --version | head -n1))"
    fi
    
    # Install ST-Link tools
    if ! command_exists st-flash; then
        print_msg "Installing ST-Link tools..."
        sudo apt-get install -y stlink-tools || {
            print_error "Failed to install ST-Link tools"
            exit 1
        }
        print_success "ST-Link tools installed"
    else
        print_success "ST-Link tools already installed ($(st-flash --version 2>&1 | head -n1))"
    fi
    
    # Install optional tools (for UART usage, not critical)
    print_msg "Installing optional tools (minicom, screen)..."
    sudo apt-get install -y minicom screen bc || print_warning "Optional tools installation failed (non-critical)"
}

# Add user to dialout group for serial port access
setup_serial_permissions() {
    print_msg "Setting up serial port permissions..."
    
    if groups | grep -q dialout; then
        print_success "User already in 'dialout' group"
    else
        print_msg "Adding user to 'dialout' group..."
        sudo usermod -a -G dialout $USER || {
            print_warning "Failed to add user to dialout group"
            return
        }
        print_success "User added to 'dialout' group"
        print_warning "You need to LOG OUT and LOG IN again for group changes to take effect!"
    fi
}

# Verify installations
verify_installation() {
    print_msg "Verifying installations..."

    local all_good=true

    if command_exists cmake; then
        print_success "✓ CMake: $(cmake --version | head -n1)"
    else
        print_error "✗ CMake not found"
        all_good=false
    fi

    if command_exists arm-none-eabi-gcc; then
        print_success "✓ ARM GCC: $(arm-none-eabi-gcc --version | head -n1)"
    else
        print_error "✗ ARM GCC not found"
        all_good=false
    fi

    if command_exists st-flash; then
        print_success "✓ ST-Link: $(st-flash --version 2>&1 | head -n1)"
    else
        print_error "✗ ST-Link not found"
        all_good=false
    fi

    if $all_good; then
        echo ""
        print_success "All dependencies installed successfully!"
        echo ""
        print_msg "Next steps:"
        echo "  1. If you were added to 'dialout' group, logout/login"
        echo "  2. Run: ./compile_flash.sh slow"
        echo ""
    else
        echo ""
        print_error "Some dependencies are missing. Please install them manually."
        exit 1
    fi
}

# Main function
main() {
    echo ""
    echo "=============================================="
    echo "  STM32 Development Dependencies Installer"
    echo "=============================================="
    echo ""

    # Detect OS
    detect_os

    # Install dependencies
    install_ubuntu_debian

    # Setup serial permissions
    setup_serial_permissions

    # Verify everything is installed
    verify_installation
}

# RUN FOREST, RUN!
main

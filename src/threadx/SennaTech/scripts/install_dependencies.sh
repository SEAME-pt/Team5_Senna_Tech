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
    
    case "$OS" in
        ubuntu|debian|linuxmint|pop)
            print_success "Debian-based system detected"
            ;;
        *)
            print_error "This script only supports Debian-based systems"
            exit 1
            ;;
    esac
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install latest ST-Link from source
install_stlink_latest() {
    print_msg "Installing latest ST-Link tools from source..."

    sudo apt-get install -y git build-essential cmake libusb-1.0-0-dev

    if command_exists st-flash; then
        print_warning "Removing old stlink-tools version..."
        sudo apt-get remove -y stlink-tools
    fi

    rm -rf stlink
    git clone https://github.com/stlink-org/stlink.git || {
        print_error "Failed to clone stlink repository"
        exit 1
    }

    cd stlink
    make release || {
        print_error "Failed to build stlink"
        exit 1
    }

    sudo make install || {
        print_error "Failed to install stlink"
        exit 1
    }

    cd ..
    rm -rf stlink

    STLINK_VERSION=$(st-flash --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
    print_success "Latest ST-Link installed (v$STLINK_VERSION)"
}

# Install dependencies
install_ubuntu_debian() {
    print_msg "Installing dependencies..."

    sudo apt-get update || { print_error "Failed to update"; exit 1; }

    if ! command_exists cmake; then
        print_msg "Installing CMake..."
        sudo apt-get install -y cmake || exit 1
    else
        print_success "CMake already installed ($(cmake --version | head -n1))"
    fi

    if ! command_exists arm-none-eabi-gcc; then
        print_msg "Installing ARM GCC toolchain..."
        sudo apt-get install -y gcc-arm-none-eabi binutils-arm-none-eabi || exit 1
    else
        print_success "ARM GCC already installed ($(arm-none-eabi-gcc --version | head -n1))"
    fi

    # Always install latest ST-Link (fix for chip ID issues)
    install_stlink_latest

    print_msg "Installing optional tools..."
    sudo apt-get install -y minicom screen bc || print_warning "Optional tools failed"
}

setup_serial_permissions() {
    print_msg "Setting up serial permissions..."
    
    if groups | grep -q dialout; then
        print_success "User already in dialout group"
    else
        sudo usermod -a -G dialout $USER
        print_warning "Added to dialout group (logout/login required)"
    fi
}

verify_installation() {
    print_msg "Verifying installations..."

    local all_good=true

    command_exists cmake && \
        print_success "✓ CMake: $(cmake --version | head -n1)" || all_good=false

    command_exists arm-none-eabi-gcc && \
        print_success "✓ ARM GCC: $(arm-none-eabi-gcc --version | head -n1)" || all_good=false

    if command_exists st-flash; then
        STLINK_VERSION=$(st-flash --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
        print_success "✓ ST-Link: v$STLINK_VERSION"
    else
        print_error "✗ ST-Link not found"
        all_good=false
    fi

    echo ""

    if $all_good; then
        print_success "All dependencies installed successfully!"
        echo ""
        print_msg "Next steps:"
        echo "  1. Logout/login if added to dialout"
        echo "  2. Run: ./compile_flash.sh slow"
    else
        print_error "Some dependencies are missing"
        exit 1
    fi
}

main() {
    echo ""
    echo "=============================================="
    echo "  STM32 Development Dependencies Installer"
    echo "=============================================="
    echo ""

    detect_os
    install_ubuntu_debian
    setup_serial_permissions
    verify_installation
}

main
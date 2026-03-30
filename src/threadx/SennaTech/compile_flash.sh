#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Resolve project directory dynamically:
# - Prefer script directory when CMakeLists.txt is present (current layout)
# - Fallback to nested SennaTech/ for legacy layout
if [ -f "$SCRIPT_DIR/CMakeLists.txt" ]; then
    PROJECT_DIR="$SCRIPT_DIR"
elif [ -f "$SCRIPT_DIR/SennaTech/CMakeLists.txt" ]; then
    PROJECT_DIR="$SCRIPT_DIR/SennaTech"
else
    echo -e "${RED}[ERROR]${NC} Could not find CMakeLists.txt in '$SCRIPT_DIR' or '$SCRIPT_DIR/SennaTech'"
    exit 1
fi

BUILD_DIR="$PROJECT_DIR/build"
BINARY_NAME="SennaTech"
FLASH_ADDRESS="0x08000000"

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

# Show usage (when -h or --help is passed)
show_usage() {
    echo "Usage: $0 [slow|fast]"
    echo ""
    echo "Arguments:"
    echo "  slow  - Full rebuild (clean build directory, run CMake, compile)"
    echo "  fast  - Quick rebuild (incremental build and flash)"
    echo ""
    echo "Examples:"
    echo "  $0 slow   # Full clean build"
    echo "  $0 fast   # Quick incremental build"
    echo "  $0        # Same as 'fast' (default)"
}

# Full rebuild from scratch (slow)
slow_build() {
    print_msg "Starting SLOW build (full rebuild)..."
    
    # Check if build directory exists
    if [ -d "$BUILD_DIR" ]; then
        print_warning "Build directory exists. Cleaning..."
        rm -rf "$BUILD_DIR"/*
        print_success "Build directory cleaned"
    else
        print_msg "Creating build directory..."
        mkdir -p "$BUILD_DIR"
        print_success "Build directory created"
    fi
    
    # cd to build directory
    cd "$BUILD_DIR" || { print_error "Failed to enter build directory"; exit 1; }
    
    # Run CMake configuration
    print_msg "Configuring CMake with ARM GCC toolchain..."
    cmake -DCMAKE_TOOLCHAIN_FILE="$PROJECT_DIR/cmake/gcc-arm-none-eabi.cmake" "$PROJECT_DIR" || {
        print_error "CMake configuration failed"
        exit 1
    }
    print_success "CMake configured successfully"
    
    # Compiling
    print_msg "Compiling project..."
    make -j$(nproc) || {
        print_error "Compilation failed"
        exit 1
    }
    print_success "Compilation completed successfully"
    
    # Convert to binary and flash
    convert_and_flash
}

# Rebuild and flash (fast)
fast_build() {
    print_msg "Starting FAST build (incremental)..."
    
    # Check if build directory exists
    if [ ! -d "$BUILD_DIR" ]; then
        print_error "Build directory not found. Run with 'slow' first."
        exit 1
    fi
    
    # cd to build directory
    cd "$BUILD_DIR" || { print_error "Failed to enter build directory"; exit 1; }
    
    # Check if Makefile exists
    if [ ! -f "Makefile" ]; then
        print_error "Makefile not found. Run with 'slow' to configure CMake first."
        exit 1
    fi
    
    # Compile project
    print_msg "Compiling project (incremental)..."
    make -j$(nproc) || {
        print_error "Compilation failed"
        exit 1
    }
    print_success "Compilation completed successfully"
    
    # Convert to binary and flash
    convert_and_flash
}

# Convert ELF to binary and flash to STM32
convert_and_flash() {
    print_msg "Converting ELF to binary..."
    arm-none-eabi-objcopy -O binary "${BINARY_NAME}.elf" "${BINARY_NAME}.bin" || {
        print_error "Binary conversion failed"
        exit 1
    }
    print_success "Binary created: ${BINARY_NAME}.bin"
    
    # Verify ST-Link connection
    print_msg "Verifying ST-Link connection..."
    st-info --probe > /dev/null 2>&1 || {
        print_error "ST-Link not detected. Please check your connection."
        exit 1
    }
    print_success "ST-Link detected"
    
    # Erase flash
    print_msg "Erasing flash memory..."
    st-flash erase || {
        print_error "Flash erase failed"
        exit 1
    }
    print_success "Flash erased"
    
    # Write binary to flash
    print_msg "Flashing binary to ${FLASH_ADDRESS}..."
    st-flash --reset write "${BINARY_NAME}.bin" ${FLASH_ADDRESS} || {
        print_error "Flash write failed"
        exit 1
    }
    print_success "Flash completed successfully!"
    
    # Show binary size
    local size=$(stat -f%z "${BINARY_NAME}.bin" 2>/dev/null || stat -c%s "${BINARY_NAME}.bin" 2>/dev/null)
    if [ -n "$size" ]; then
        print_msg "Binary size: $size bytes ($(echo "scale=2; $size/1024" | bc) KB)"
    fi
}

# Main script logic
main() {
    echo ""
    echo "========================================="
    echo "  STM32 ThreadX Build & Flash Script"
    echo "========================================="
    echo ""
    
    # Check for required tools
    local missing_deps=false
    local missing_tools=""
    
    if ! command -v arm-none-eabi-gcc >/dev/null 2>&1; then
        print_error "arm-none-eabi-gcc not found"
        missing_deps=true
        missing_tools="${missing_tools}- ARM GCC toolchain (arm-none-eabi-gcc)\n"
    fi
    
    if ! command -v cmake >/dev/null 2>&1; then
        print_error "cmake not found"
        missing_deps=true
        missing_tools="${missing_tools}- CMake\n"
    fi
    
    if ! command -v st-flash >/dev/null 2>&1; then
        print_error "st-flash not found"
        missing_deps=true
        missing_tools="${missing_tools}- ST-Link tools (stlink-tools)\n"
    fi
    
    if $missing_deps; then
        echo ""
        print_warning "Missing dependencies:"
        echo -e "$missing_tools"
        
        if [ -f "$SCRIPT_DIR/install_dependencies.sh" ]; then
            echo ""
            read -p "Would you like to run the dependency installer? (y/n): " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                print_msg "Running install_dependencies.sh..."
                bash "$SCRIPT_DIR/install_dependencies.sh" || {
                    print_error "Dependency installation failed"
                    exit 1
                }
                print_success "Dependencies installed. Please re-run this script."
                exit 0
            else
                print_error "Cannot proceed without required dependencies"
                exit 1
            fi
        else
            print_error "install_dependencies.sh not found in $SCRIPT_DIR"
            print_msg "Please install dependencies manually or download install_dependencies.sh"
            exit 1
        fi
    fi
    
    # Parse arguments
    case "${1:-fast}" in
        slow)
            slow_build
            ;;
        fast)
            fast_build
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Invalid argument: $1"
            echo ""
            show_usage
            exit 1
            ;;
    esac
    
    echo ""
    print_success "All operations completed successfully!"
    echo ""
}

# Run main function
main "$@"

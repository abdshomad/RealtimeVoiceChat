#!/bin/bash

# RealTimeVoiceChat Installation Script for Linux/Unix
# Uses uv for package management and .venv for virtual environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python version
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
        REQUIRED_VERSION="3.10"
        
        if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
            print_success "Python version $PYTHON_VERSION is compatible"
        else
            print_error "Python version $PYTHON_VERSION is too old. Required: >=$REQUIRED_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    # Check for system dependencies
    print_status "Checking for system dependencies..."
    
    # Check for build tools
    if ! command_exists gcc; then
        print_warning "gcc not found. Installing build-essential..."
        sudo apt-get update && sudo apt-get install -y build-essential
    else
        print_success "gcc found"
    fi
    
    # Check for Python dev headers
    if [ ! -f "/usr/include/python3.11/Python.h" ] && [ ! -f "/usr/include/python3.10/Python.h" ]; then
        print_warning "Python development headers not found. Installing python3-dev..."
        sudo apt-get update && sudo apt-get install -y python3-dev
    else
        print_success "Python development headers found"
    fi
    
    # Check for audio libraries
    if ! command_exists pkg-config; then
        print_warning "pkg-config not found. Installing pkg-config..."
        sudo apt-get update && sudo apt-get install -y pkg-config
    else
        print_success "pkg-config found"
    fi
    
    # Check if uv is installed
    if ! command_exists uv; then
        print_warning "uv is not installed. Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source $HOME/.cargo/env
    else
        print_success "uv is already installed"
    fi
    
    # Check for CUDA (optional but recommended)
    if command_exists nvidia-smi; then
        print_success "NVIDIA GPU detected"
        nvidia-smi --query-gpu=name --format=csv,noheader,nounits | while read gpu; do
            print_status "GPU: $gpu"
        done
    else
        print_warning "NVIDIA GPU not detected. Performance may be slower."
    fi
    
    # Check for Docker (optional)
    if command_exists docker; then
        print_success "Docker is available"
    else
        print_warning "Docker not found. Consider installing for easier deployment."
    fi
}

# Function to install uv if not present
install_uv() {
    if ! command_exists uv; then
        print_status "Installing uv package manager..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source $HOME/.cargo/env
        print_success "uv installed successfully"
    fi
}

# Function to setup virtual environment
setup_venv() {
    print_status "Setting up virtual environment with uv..."
    
    # Check if .venv exists
    if [ -d ".venv" ]; then
        print_status "Using existing virtual environment..."
    else
        print_status "Creating new virtual environment..."
    fi
    
    # Install/update dependencies in virtual environment
    uv sync
    print_success "Virtual environment dependencies installed/updated"
}

# Function to verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    # Activate virtual environment and test imports
    source .venv/bin/activate
    
    # Test key dependencies
    python3 -c "
import sys
print(f'Python version: {sys.version}')

try:
    import numpy
    print(f'NumPy version: {numpy.__version__}')
except ImportError as e:
    print(f'NumPy import error: {e}')

try:
    import torch
    print(f'PyTorch version: {torch.__version__}')
    if torch.cuda.is_available():
        print(f'CUDA available: {torch.cuda.get_device_name(0)}')
    else:
        print('CUDA not available')
except ImportError as e:
    print(f'PyTorch import error: {e}')

try:
    import RealtimeSTT
    print('RealtimeSTT imported successfully')
except ImportError as e:
    print(f'RealtimeSTT import error: {e}')

try:
    import RealtimeTTS
    print('RealtimeTTS imported successfully')
except ImportError as e:
    print(f'RealtimeTTS import error: {e}')

try:
    from RealtimeTTS import CoquiEngine, KokoroEngine, OrpheusEngine
    print('RealtimeTTS engines imported successfully')
except ImportError as e:
    print(f'RealtimeTTS engines import error: {e}')

try:
    import fastapi
    print('FastAPI imported successfully')
except ImportError as e:
    print(f'FastAPI import error: {e}')

try:
    import librosa
    print('Librosa imported successfully')
except ImportError as e:
    print(f'Librosa import error: {e}')

try:
    import soundfile
    print('SoundFile imported successfully')
except ImportError as e:
    print(f'SoundFile import error: {e}')
"
    
    print_success "Installation verification completed"
}



# Function to display next steps
show_next_steps() {
    echo ""
    print_success "Installation completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Start the server: ./run_server.sh"
    echo "2. Open your browser to: http://localhost:8000"
    echo "3. Grant microphone permissions when prompted"
    echo "4. Click 'Start' to begin chatting!"
    echo ""
    echo "Optional:"
    echo "- For Docker deployment: docker compose up -d"
    echo "- For GPU optimization: Ensure CUDA drivers are installed"
    echo "- For production: Review docs/PRD.md for deployment guidelines"
    echo ""
}

# Main installation process
main() {
    echo "=========================================="
    echo "RealTimeVoiceChat Installation Script"
    echo "=========================================="
    echo ""
    
    # Check if we're in the right directory
    if [ ! -f "pyproject.toml" ]; then
        print_error "pyproject.toml not found. Please run this script from the project root directory."
        exit 1
    fi
    
    # Check system requirements
    check_requirements
    
    # Install uv if needed
    install_uv
    
    # Setup virtual environment
    setup_venv
    
    # Verify installation
    verify_installation
    
    # Show next steps
    show_next_steps
}

# Run main function
main "$@" 
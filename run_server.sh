#!/bin/bash

# RealTimeVoiceChat Server Runner
# Activates virtual environment and starts the server

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found. Run install.sh first."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if required modules are available
echo "Checking dependencies..."
python -c "
try:
    from RealtimeSTT import AudioToTextRecorderClient
    print('✅ RealtimeSTT available')
except ImportError as e:
    print(f'❌ Missing RealtimeSTT dependency: {e}')
    print('Please run install.sh to install all dependencies')
    exit(1)

try:
    from RealtimeTTS import CoquiEngine, OrpheusEngine
    print('✅ RealtimeTTS core engines available')
except ImportError as e:
    print(f'⚠️  Some RealtimeTTS engines not available: {e}')
    print('This is normal if optional dependencies are not installed')

try:
    from RealtimeTTS import KokoroEngine
    print('✅ KokoroEngine available')
except ImportError as e:
    print('⚠️  KokoroEngine not available (optional)')
    print('To install: pip install realtimetts[kokoro]')

print('✅ Core dependencies available - server can start')
"

# Load environment variables from .env file
if [ -f ".env" ]; then
    echo "Loading configuration from .env file..."
    export $(grep -v '^#' .env | xargs)
else
    echo "Warning: .env file not found, using default configuration"
fi

# Set default PORT if not defined
export PORT=${PORT:-9000}
export HOST=${HOST:-0.0.0.0}

# Ensure logs directory exists
mkdir -p logs
echo "📁 Logs directory ready: ./logs/"

# Navigate to code directory
cd code

# Start the server
echo "Starting RealTimeVoiceChat server..."
echo "Access the application at: http://localhost:${PORT}"
echo "📁 Server logs will be saved to: ../logs/"
echo "Press Ctrl+C to stop the server"
echo ""

python server.py

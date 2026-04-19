#!/bin/bash

echo "🛡️  Toxicity Detector - Development Server"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ============================================================================
# STEP 1: Start Backend
# ============================================================================
echo "📍 STEP 1: Starting Backend..."
echo "Going to: backend/"
cd "$PROJECT_ROOT/backend"

# Activate venv
source ../venv/bin/activate

# Check if port 8000 is in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${RED}❌ Port 8000 is already in use!${NC}"
    echo "Either:"
    echo "  1. Kill the process using port 8000"
    echo "  2. Or use a different port"
    echo ""
    echo "To kill process on port 8000:"
    echo "  kill -9 \$(lsof -t -i :8000)"
    exit 1
else
    echo -e "${GREEN}✅ Port 8000 is available${NC}"
    echo "Starting Flask server..."
    python app.py &
    BACKEND_PID=$!
    sleep 2
    echo -e "${GREEN}✅ Backend started on http://localhost:8000${NC}"
fi

echo ""

# ============================================================================
# STEP 2: Start Frontend
# ============================================================================
echo "📍 STEP 2: Starting Frontend..."
echo "Going to: frontend/"
cd "$PROJECT_ROOT/frontend"

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install -q
    echo -e "${GREEN}✅ Dependencies installed${NC}"
fi

echo "Starting Vite dev server..."
npm start &
FRONTEND_PID=$!
sleep 3

echo ""
echo "=========================================="
echo -e "${GREEN}🚀 Both servers are running!${NC}"
echo "=========================================="
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend:  http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/api/info"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for both processes
wait

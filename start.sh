#!/bin/bash

echo "🚀 Starting MasterCRM Repo Tool - Optimized Edition"
echo "=================================================="
echo ""

# Check if port 8501 is already in use
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8501 is already in use. Killing existing process..."
    lsof -ti:8501 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# Check if dependencies are installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Start the app
echo "✨ Launching app on http://localhost:8501"
echo "=================================================="
echo ""

streamlit run app.py --server.port=8501 --server.headless=false

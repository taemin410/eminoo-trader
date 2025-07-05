#!/bin/bash

echo "🚀 Starting Trading Dashboard..."

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Start the dashboard
echo "🌐 Starting FastAPI server on port 8000..."
echo "📊 Dashboard will be available at: http://your-ec2-ip:8000"
echo "📚 API docs available at: http://your-ec2-ip:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"

python dashboard.py 
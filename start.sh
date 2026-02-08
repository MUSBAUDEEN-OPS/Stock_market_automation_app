#!/bin/bash

# Quick Start Script for Stock Predictor App
# This script sets up and runs the app locally

echo "🚀 Stock Market Predictor - Quick Start"
echo "========================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found."
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your email credentials."
    echo ""
fi

# Create subscribers.json if it doesn't exist
if [ ! -f "subscribers.json" ]; then
    echo "📧 Creating subscribers file..."
    echo "[]" > subscribers.json
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌟 Starting Streamlit app..."
echo "   The app will open in your browser at http://localhost:8501"
echo ""
echo "💡 To stop the app, press Ctrl+C"
echo ""

# Run the app
streamlit run app.py

#!/bin/bash
# Setup script for Face Scanner

echo "=========================================="
echo "Face Scanner Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo "✓ Python dependencies installed"
echo ""

# Download dlib facial landmark predictor if not exists
if [ ! -f "shape_predictor_68_face_landmarks.dat" ]; then
    echo "📥 Downloading dlib facial landmark predictor..."
    wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to download facial landmark predictor"
        echo "Please download manually from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
        exit 1
    fi
    
    echo "📦 Extracting..."
    bunzip2 shape_predictor_68_face_landmarks.dat.bz2
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to extract facial landmark predictor"
        exit 1
    fi
    
    echo "✓ Facial landmark predictor downloaded and extracted"
else
    echo "✓ Facial landmark predictor already exists"
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To register a user:"
echo "  python3 face_scanner.py --register username"
echo ""
echo "To start face recognition:"
echo "  python3 face_scanner.py"
echo ""


# Installation Guide

## Quick Start

### 1. Create Virtual Environment

```bash
cd /home/justdial/Documents/face_scanner
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: Installing `dlib` and `torch` may take several minutes.

### 3. Download Required Models

#### Facial Landmark Predictor (Required)
```bash
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
```

#### Anti-Spoofing Model (Optional, Recommended)
The system works with heuristic-based anti-spoofing by default. For better accuracy, you can download a pre-trained model:

1. Visit: https://github.com/minivision-ai/Silent-Face-Anti-Spoofing
2. Download the ONNX model file
3. Place it in the project directory as `antispoofing_model.onnx`

If no model is found, the system will use the built-in heuristic fallback.

### 4. Run the System

#### Register a user:
```bash
python face_scanner.py --register your_username
```

#### Start face recognition:
```bash
python face_scanner.py
```

## System Dependencies (Linux)

```bash
sudo apt-get update
sudo apt-get install -y cmake build-essential
sudo apt-get install -y libopenblas-dev liblapack-dev
sudo apt-get install -y libx11-dev libgtk-3-dev
```

## How It Works

### Anti-Spoofing Detection

The system uses two modes:

1. **Deep Learning Mode** (when model is available):
   - Uses ONNX neural network
   - Trained on thousands of real vs fake face images
   - High accuracy detection

2. **Heuristic Mode** (fallback):
   - Multi-feature analysis:
     * Color diversity
     * Texture richness
     * Edge sharpness
     * Frequency domain analysis
     * Lighting consistency
   - Combines multiple indicators for spoof detection

### Recognition Flow

```
Motion Detected
    ↓
Face Detected & Matched
    ↓
AI Anti-Spoofing Check → [FAKE? → ACCESS DENIED]
    ↓ [REAL]
Blink Verification → [NO BLINK? → ACCESS DENIED]
    ↓ [BLINK DETECTED]
ACCESS GRANTED
```

## Troubleshooting

### "torch not installed"
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### "onnxruntime not found"
```bash
pip install onnxruntime
```

### Anti-spoofing always uses heuristic mode
- This is normal if you haven't downloaded the ONNX model
- Heuristic mode is still effective against most attacks
- For best results, download a pre-trained model (see step 3 above)

## Performance

- **With Deep Learning Model**: ~50-100ms per anti-spoof check
- **With Heuristic Mode**: ~10-20ms per anti-spoof check
- **Overall Recognition**: 1-2 seconds from motion to access decision

## Security Notes

- The heuristic mode effectively detects photos, low-quality videos, and screen displays
- Deep learning mode provides additional protection against sophisticated attacks
- Blink verification adds an extra layer of liveness confirmation
- System is designed to err on the side of caution (false rejection over false acceptance)


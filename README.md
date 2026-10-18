# Face Scanner with Motion Detection and Liveness Check

A complete Python-based face registration and recognition system with motion detection and liveness verification for access control applications.

## Features

- **Face Registration**: Register users with liveness detection (blink verification)
- **Motion Detection**: Continuously monitors for motion before scanning for faces
- **AI Anti-Spoofing**: Deep learning-based detection of photos/videos/masks
- **Face Recognition**: Compares detected faces against registered users
- **Visual Feedback**: Green overlay for granted access, red for denied
- **Liveness Verification**: Simple blink detection for interactive verification
- **Auto Directory Management**: Automatically creates necessary directories

## Requirements

- Python 3.7 or higher
- USB webcam
- Linux, Windows, or macOS

## Installation

### 1. Install System Dependencies (Linux)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-pip cmake build-essential
sudo apt-get install -y libopencv-dev python3-opencv
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: Installing `dlib` may take several minutes as it compiles from source.

### 3. Download Facial Landmark Predictor

Download the dlib facial landmark predictor model:

```bash
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
```

This will create `shape_predictor_68_face_landmarks.dat` in your current directory.

## Usage

### Register a New User

```bash
python face_scanner.py --register username
```

**Instructions during registration:**
1. Look at the camera
2. **Blink your eyes naturally AT LEAST 2 TIMES** (photos won't work!)
3. The system will capture 5 images during your blinks
4. Press 'Q' to cancel

**Anti-Spoofing:** The system requires detecting at least 2 complete blink cycles (eyes open → closed → open) to prevent registration using photos or static images.

User data will be saved in the `users/` directory as `username.pickle`.

### Start Face Recognition System

```bash
python face_scanner.py
```

**Example Console Output:**

```
🔔 Motion detected! Scanning for faces...
   Found 1 face(s) in frame
   Best match distance: 0.412 (confidence: 58.8%)
   Potential match: john (confidence: 58.8%)
   🤖 Running AI anti-spoofing detection...
      Method: heuristic
      Prediction: FAKE
      Confidence: 72%
      Spoof score: 72%
   ⚠ SPOOFING DETECTED!
✗ ACCESS DENIED: Face appears to be fake (photo/video/mask)
```

**How it works:**
1. The system monitors for motion using frame differencing
2. When motion is detected, it scans for faces
3. Detected faces are compared against all registered users
4. If a potential match is found (face encoding + confidence check):
   - **SCREEN DETECTION**: Analyzes face region for display patterns using FFT
   - **LIVENESS VERIFICATION**: System prompts "PLEASE BLINK TO VERIFY"
   - User has 5 seconds to blink
   - System detects complete blink cycle: eyes open → closed → open
   - Shows real-time feedback with eye status and EAR value
5. If screen not detected AND blink verified AND face matches:
   - Displays "ACCESS GRANTED: [username]"
   - Shows green overlay
   - Prints "Door Unlocked!"
   - Displays for 5 seconds
6. If screen detected OR no blink OR no face match:
   - Displays "ACCESS DENIED"
   - Shows red overlay
   - Displays specific reason:
     - "Screen Detected" (phone/monitor display)
     - "Liveness Failed" (no blink detected)
     - "Unknown face" (not registered)
   - Displays for 5 seconds
7. Returns to motion monitoring after each attempt
8. Press 'Q' to quit

## Configuration

You can adjust these constants in `face_scanner.py`:

```python
EYE_AR_THRESHOLD = 0.21        # Blink detection sensitivity (lower = stricter)
EYE_AR_CONSEC_FRAMES = 3       # Consecutive frames needed to confirm blink
EYE_AR_OPEN_THRESHOLD = 0.25   # Threshold for eyes being open
REQUIRED_BLINKS = 2            # Minimum blinks required during registration
MOTION_THRESHOLD = 25          # Motion detection sensitivity
MOTION_MIN_AREA = 500          # Minimum area to count as motion
RECOGNITION_TOLERANCE = 0.5    # Face match distance tolerance (lower = stricter)
MIN_CONFIDENCE = 0.55          # Minimum confidence to grant access (higher = stricter)
ACCESS_DISPLAY_TIME = 5        # Seconds to display access result
```

**Important:** Lower values for `RECOGNITION_TOLERANCE` and higher values for `MIN_CONFIDENCE` make the system more secure but may increase false negatives (rejecting legitimate users).

## Troubleshooting

### "ERROR: opencv-python is not installed"
```bash
pip install opencv-python
```

### "ERROR: face_recognition library is not installed"
```bash
pip install face_recognition
```

### "ERROR: dlib or scipy is not installed"
```bash
pip install dlib scipy
```

### "ERROR: Could not load facial landmark predictor"

Download the model file:
```bash
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
```

### "ERROR: Could not open webcam"

- Check if your webcam is connected
- Ensure no other application is using the webcam
- Try changing the camera index in the code (replace `cv2.VideoCapture(0)` with `cv2.VideoCapture(1)`)

### Dlib Installation Issues

If dlib fails to install via pip:

**On Ubuntu/Debian:**
```bash
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
pip install dlib
```

**On macOS:**
```bash
brew install cmake
pip install dlib
```

## Project Structure

```
face_scanner/
├── face_scanner.py                          # Main script
├── requirements.txt                         # Python dependencies
├── README.md                               # This file
├── shape_predictor_68_face_landmarks.dat   # dlib model (download separately)
└── users/                                  # Registered user data (auto-created)
    ├── username1.pickle
    ├── username2.pickle
    └── ...
```

## How It Works

### Registration Process

1. Opens webcam and initializes dlib face detector
2. Detects facial landmarks (68 points)
3. Implements blink state machine to track complete blink cycles:
   - Detects when eyes are open (EAR > 0.25)
   - Detects when eyes close (EAR < 0.21)
   - Tracks transition from open → closed → open as one complete blink
4. **Requires at least 2 complete blinks** to prevent photo spoofing
5. Captures 5 face images **when eyes reopen after each blink** (not during the blink)
   - This ensures encodings match recognition conditions (eyes open)
   - Captures with 0.5 second cooldown between frames
6. Extracts face encodings using face_recognition library
7. Validates liveness before saving encodings to `users/username.pickle`

### Recognition Process

1. Loads all registered user encodings
2. Continuously monitors webcam for motion
3. Compares current frame with previous frame
4. When motion detected:
   - Scans for faces in the frame
   - Extracts face encodings
   - Compares with known encodings using distance metric
   - Checks confidence threshold (must be ≥ 55%)
5. If potential match found:
   - **Multi-Layer Video/Screen Detection** (7 methods):
     - Extracts face ROI (Region of Interest)
     - **Method 1 - FFT Analysis**: Detects moiré patterns from screen pixel grids
     - **Method 2 - Edge Sharpness**: Screens have unnaturally sharp edges
     - **Method 3 - Color Saturation**: Checks for over/under-saturated colors
     - **Method 4 - Brightness Uniformity**: Detects screen backlighting
     - **Method 5 - Texture Analysis**: Real skin has micro-textures screens lack
     - **Method 6 - Color Temperature**: Validates skin tones in Lab color space
     - **Method 7 - Temporal Patterns**: Detects video loops and unnatural motion
     - If any method triggers → immediate denial with specific reason
   - **Liveness Verification** (only if passes video detection):
     - Prompts: "PLEASE BLINK TO VERIFY"
     - User has 5 seconds to respond
     - Detects complete blink cycle (eyes open → closed → open)
     - Shows real-time eye status and EAR value
6. Access decision:
   - ✅ **GRANTED**: Face matches AND no video/screen detected AND blink verified
   - ❌ **DENIED**: Unknown face OR video/screen detected OR no blink
7. Returns to monitoring after brief cooldown

**Key Security Features**:
1. **7-Layer Video Detection**: Multiple independent methods ensure high accuracy
2. **FFT Moiré Detection**: Catches screen pixel grid patterns
3. **Color Space Analysis**: HSV and Lab color spaces reveal display artifacts
4. **Texture & Edge Analysis**: Differentiates real skin from digital reproduction
5. **Temporal Analysis**: Detects video playback patterns and loops
6. **Liveness Check**: Final verification requires real-time blink
7. **Layered Defense**: Even if one method fails, others provide backup

### Liveness Detection (Two-Phase Protection)

**Phase 1: Registration Liveness**
- **Blink Detection**: Uses Eye Aspect Ratio (EAR) calculation with state machine
  - Measures ratio of vertical to horizontal eye landmarks (6 points per eye)
  - Tracks complete blink cycles: open (EAR > 0.25) → closed (EAR < 0.21) → open
  - Requires consecutive frames to confirm blink (reduces false positives)
  - **Minimum 2 complete blinks required** during registration
  - Captures face encodings when eyes reopen after blinks
  - Prevents registering using photos

**Phase 2: Recognition Liveness (Multi-Method Video Detection + Blink Check)**
- When a face matches a registered user:
  - **7-Layer Video/Screen Detection System**:
  
    1. **FFT Moiré Pattern Detection**
       - Analyzes frequency domain of face image
       - Screens have regular pixel grids creating periodic patterns
       - Detects high-frequency variance characteristic of displays
    
    2. **Edge Sharpness Analysis**
       - Uses Canny edge detection
       - Screens produce unnaturally sharp edges
       - Measures edge density ratio
    
    3. **Color Saturation Check**
       - Analyzes HSV color space
       - Screens often over-saturate or under-saturate colors
       - Real skin has specific saturation characteristics
    
    4. **Brightness Uniformity**
       - Screen backlighting creates unnatural uniformity
       - Real faces have natural shadow variations
       - Measures brightness variance
    
    5. **Texture Analysis**
       - Real skin has micro-textures (pores, fine lines)
       - Screens smooth these out or can't reproduce them
       - Uses Laplacian variance to measure texture
    
    6. **Color Temperature Validation**
       - Analyzes Lab color space (L*, a*, b*)
       - Real skin has specific color temperature range
       - a* channel: 145-165, b* channel: 130-150 typical
       - Screens often shift these values
    
    7. **Temporal Pattern Analysis**
       - Tracks face movement across frames
       - Video loops have too-perfect consistency
       - Screen shake creates unnatural motion patterns
       - Real people have natural micro-movements
  
  - **Interactive Challenge-Response** (only if passes all video checks):
    - System randomly selects **2 different challenges** from:
      * "BLINK" - Close and open eyes
      * "TURN HEAD LEFT" - Turn head to the left
      * "TURN HEAD RIGHT" - Turn head to the right
    - Challenges displayed prominently on screen
    - User must complete each challenge within 5 seconds
    - Must pass BOTH challenges sequentially
    - **Videos cannot respond to random on-screen instructions**
  
**Why This Multi-Layer Approach Works**:

| Attack | Detection Layers Triggered | Result |
|--------|---------------------------|--------|
| **Photos** | No blink in challenge | ❌ Rejected |
| **Printed Images** | Texture analysis + challenge fail | ❌ Rejected |
| **Phone Video (Simple)** | FFT moiré + edge sharpness + color temp | ❌ Rejected |
| **Phone Video (HD)** | Cannot respond to random challenges | ❌ Rejected |
| **Monitor Display** | FFT moiré + brightness uniformity + texture | ❌ Rejected |
| **Tablet Video** | Cannot respond to random challenges | ❌ Rejected |
| **HD Screen Video** | Cannot respond to random on-screen instructions | ❌ Rejected |
| **Video Loop** | Wrong actions OR temporal pattern detected | ❌ Rejected |
| **Video of Blinking** | May have blink but won't have head turns | ❌ Rejected |
| **Video with Head Movement** | Wrong direction OR wrong sequence | ❌ Rejected |
| **Real Person** | All checks pass + completes random challenges | ✅ Accepted |

**Security Layers**:
1. **Face encoding match** (biometric authentication)
2. **7 independent video detection methods** (redundant anti-spoofing)
3. **Interactive challenge-response** (random on-screen instructions)
4. **Multi-action verification** (2 sequential challenges: blink + head movement)
5. **Temporal analysis** (detects playback patterns)

**Defense in Depth**: Even if an attacker bypasses video detection with a perfect screen, they cannot pass the interactive challenge-response system. Pre-recorded videos cannot:
- Know which random challenges will be shown
- Perform the exact sequence requested (e.g., blink THEN turn left)
- Have the correct head movements in the correct order
- Respond to real-time on-screen instructions

**Why Videos Fail**:
- A video with blinking won't have head turns in the right direction
- A video with head movement won't have blinks at the right moment
- The random selection means different challenges each time
- Even a collection of videos can't match the specific sequence shown

## Security Considerations

This system implements **AI-powered anti-spoofing** protection:

### Implemented Security Features ✅
1. **AI Anti-Spoofing Detection**:
   - **Deep Learning Model**: ONNX-based neural network trained on real vs fake faces
   - **Heuristic Fallback**: Multi-feature analysis when model unavailable
   - **Detects**: Photos, videos, printed images, digital displays, 3D masks
   - **Real-time Analysis**: Fast inference on each face detection
2. **Two-Phase Liveness**: Both registration and recognition require liveness
3. **Blink Verification**: Simple, reliable eye movement detection
4. **Confidence Thresholding**: Minimum 55% match confidence required
5. **Motion Detection**: Reduces unnecessary processing and false triggers

### Attack Resistance
| Attack Type | Defense Method(s) | Status |
|------------|------------------|--------|
| High-res Photo | Blink detection | ✅ Blocked |
| Printed Photo | Blink detection | ✅ Blocked |
| Phone/Screen Display | FFT + texture + color analysis | ✅ Strongly Blocked |
| Pre-recorded Video | 7-layer detection (FFT, texture, color, temporal, etc.) | ✅ Strongly Blocked |
| Tablet Display | Multi-method screen detection | ✅ Strongly Blocked |
| Video Loop | Temporal consistency analysis | ✅ Blocked |
| Low-quality Video | Edge sharpness + artifact detection | ✅ Blocked |
| High-quality Video | Multi-layer analysis (FFT, color temp, texture) | ✅ Mostly Blocked |
| 3D Mask | Basic (eye movement only) | ⚠️ Partial |
| Deepfake Video | Multi-method + liveness check | ⚠️ Partial |

### For Production Use, Consider Adding:
- 3D depth sensing (structured light, time-of-flight cameras)
- Advanced texture analysis (detect skin vs screen)
- Infrared liveness detection
- Multiple factor authentication (PIN + face)
- Encrypted storage for face encodings
- Comprehensive audit logging
- Tamper detection for camera hardware
- Regular security updates and model retraining

### Current Limitations
- **3D Masks with Animatronics**: System relies primarily on eye movement and screen detection. Sophisticated 3D masks with animatronic eyes and proper skin texture could potentially bypass (extremely rare and expensive - $10,000+)
- **Advanced Deepfakes**: Cutting-edge real-time deepfake systems running on high-end hardware might adapt to liveness checks (nation-state level attack, not common)
- **Lighting Conditions**: 
  - Poor lighting may affect face detection accuracy
  - Very bright backlighting might interfere with liveness detection
  - Extreme darkness reduces video detection accuracy
- **Professional Video Systems**: High-end projection systems or specialized displays might reduce some video detection signatures, but temporal and texture analysis should still catch them

## License

This project is provided as-is for educational and demonstration purposes.

## Credits

Built with:
- [face_recognition](https://github.com/ageitgey/face_recognition) - Face detection and encoding
- [dlib](http://dlib.net/) - Facial landmark detection
- [OpenCV](https://opencv.org/) - Computer vision and camera handling


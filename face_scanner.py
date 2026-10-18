#!/usr/bin/env python3
"""
Face Scanner - Simple Face Recognition System
==============================================
A face registration and recognition system with motion detection
and basic blink-based liveness detection.

Usage:
    # Register a new user
    python face_scanner.py --register username
    
    # Run face recognition with motion detection
    python face_scanner.py
"""

import argparse
import os
import pickle
import serial
import sys
import time
from pathlib import Path
from typing import List, Tuple, Optional, Dict

# Try to import required libraries with helpful error messages
try:
    import cv2
except ImportError:
    print("ERROR: opencv-python is not installed.")
    print("Install it with: pip install opencv-python")
    sys.exit(1)

try:
    import face_recognition
except ImportError:
    print("ERROR: face_recognition library is not installed.")
    print("Install it with: pip install face_recognition")
    sys.exit(1)

try:
    import dlib
    from scipy.spatial import distance as dist
except ImportError:
    print("ERROR: dlib or scipy is not installed.")
    print("Install them with: pip install dlib scipy")
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("ERROR: numpy is not installed.")
    print("Install it with: pip install numpy")
    sys.exit(1)

# Constants
USERS_DIR = "users"
EYE_AR_THRESHOLD = 0.21  # Eye Aspect Ratio threshold for blink detection
EYE_AR_CONSEC_FRAMES = 3  # Consecutive frames below threshold to count as blink
EYE_AR_OPEN_THRESHOLD = 0.25  # Threshold for eyes being open
REQUIRED_BLINKS = 2  # Minimum number of blinks required during registration
MOTION_THRESHOLD = 25  # Threshold for motion detection
MOTION_MIN_AREA = 500  # Minimum contour area to consider as motion
RECOGNITION_TOLERANCE = 0.5  # Face recognition tolerance (lower = stricter)
MIN_CONFIDENCE = 0.55  # Minimum confidence (1 - distance) to grant access
ACCESS_DISPLAY_TIME = 3  # Seconds to display access result

# ESP32 Serial Configuration
ESP32_PORT = "/dev/ttyUSB0"
ESP32_BAUD = 115200


def init_esp32() -> Optional[serial.Serial]:
    """Initialize serial connection to ESP32."""
    try:
        ser = serial.Serial(ESP32_PORT, ESP32_BAUD, timeout=1)
        time.sleep(2)  # Wait for ESP32 to reset after serial connection
        print(f"✓ ESP32 connected on {ESP32_PORT}")
        return ser
    except Exception as e:
        print(f"⚠ ESP32 not connected ({e}) - continuing without display")
        return None


def send_to_esp32(ser: Optional[serial.Serial], message: str):
    """Send a message to ESP32 over serial."""
    if ser and ser.is_open:
        try:
            ser.write((message + "\n").encode())
            ser.flush()
        except Exception:
            pass

# Facial landmarks indices for eyes (dlib 68-point model)
LEFT_EYE_INDICES = list(range(36, 42))
RIGHT_EYE_INDICES = list(range(42, 48))


def calculate_eye_aspect_ratio(eye_points: np.ndarray) -> float:
    """
    Calculate the Eye Aspect Ratio (EAR) for blink detection.
    """
    # Vertical distances
    A = dist.euclidean(eye_points[1], eye_points[5])
    B = dist.euclidean(eye_points[2], eye_points[4])
    # Horizontal distance
    C = dist.euclidean(eye_points[0], eye_points[3])
    # EAR formula
    ear = (A + B) / (2.0 * C)
    return ear


def ensure_users_directory():
    """Create users directory if it doesn't exist."""
    if not os.path.exists(USERS_DIR):
        os.makedirs(USERS_DIR)
        print(f"Created directory: {USERS_DIR}")


def get_registered_users() -> List[str]:
    """Get list of registered usernames."""
    ensure_users_directory()
    users = []
    for filename in os.listdir(USERS_DIR):
        if filename.endswith('.pickle'):
            users.append(filename[:-7])  # Remove .pickle extension
    return users


def save_user_encodings(username: str, encodings: List) -> bool:
    """Save face encodings for a user."""
    ensure_users_directory()
    filepath = os.path.join(USERS_DIR, f"{username}.pickle")
    
    try:
        data = {
            'username': username,
            'encodings': encodings,
            'timestamp': time.time()
        }
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        return True
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False


def load_user_encodings(username: str) -> Optional[List]:
    """Load face encodings for a user."""
    filepath = os.path.join(USERS_DIR, f"{username}.pickle")
    
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            return data.get('encodings', [])
    except Exception as e:
        print(f"Error loading user data: {e}")
        return None


def register_user(username: str) -> bool:
    """
    Register a new user by capturing face encodings.
    Requires user to blink to prove liveness.
    """
    print(f"\n{'='*60}")
    print(f"REGISTERING USER: {username}")
    print(f"{'='*60}")
    
    # Check if user already exists
    if username in get_registered_users():
        print(f"⚠ User '{username}' already exists!")
        response = input("Overwrite? (y/n): ").lower()
        if response != 'y':
            print("Registration cancelled.")
            return False
    
    # Initialize dlib's face detector and landmark predictor
    detector = dlib.get_frontal_face_detector()
    
    # Download predictor if not exists
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    if not os.path.exists(predictor_path):
        print(f"\n⚠ Facial landmark predictor not found!")
        print(f"Please download it from:")
        print(f"http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
        print(f"Extract and place in: {os.getcwd()}")
        return False
    
    predictor = dlib.shape_predictor(predictor_path)
    
    # Open webcam
    print("\n📷 Initializing webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Could not open webcam!")
        return False
    
    print("✓ Webcam ready!")
    print("\nINSTRUCTIONS:")
    print(f"  1. Look at the camera")
    print(f"  2. Blink {REQUIRED_BLINKS} times to prove you're real")
    print(f"  3. Keep looking at the camera while images are captured")
    print("\nPress 'q' to cancel registration\n")
    
    encodings = []
    captured_frames = 0
    total_frames_needed = 10
    blink_count = 0
    eyes_closed = False
    last_capture_time = 0
    capture_interval = 0.3
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to read from webcam")
            break
        
        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        display_frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = detector(gray, 0)
        
        if len(faces) == 0:
            cv2.putText(display_frame, "No face detected - please look at camera", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            face = faces[0]
            shape = predictor(gray, face)
            shape_np = np.array([[shape.part(i).x, shape.part(i).y] for i in range(68)])
            
            # Get eye points
            left_eye = shape_np[LEFT_EYE_INDICES]
            right_eye = shape_np[RIGHT_EYE_INDICES]
            
            # Calculate EAR
            left_ear = calculate_eye_aspect_ratio(left_eye)
            right_ear = calculate_eye_aspect_ratio(right_eye)
            ear = (left_ear + right_ear) / 2.0
            
            # Blink detection
            if ear < EYE_AR_THRESHOLD:
                if not eyes_closed:
                    eyes_closed = True
            else:
                if eyes_closed:
                    blink_count += 1
                    print(f"👁️  Blink detected! ({blink_count}/{REQUIRED_BLINKS})")
                    eyes_closed = False
            
            # Draw face rectangle
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Capture face if blinks verified and enough time passed
            current_time = time.time()
            if blink_count >= REQUIRED_BLINKS and captured_frames < total_frames_needed:
                if current_time - last_capture_time >= capture_interval and ear > EYE_AR_OPEN_THRESHOLD:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    face_locations = face_recognition.face_locations(rgb_frame)
                    
                    if len(face_locations) > 0:
                        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                        if len(face_encodings) > 0:
                            encodings.append(face_encodings[0])
                            captured_frames += 1
                            last_capture_time = current_time
                            print(f"✓ Captured image {captured_frames}/{total_frames_needed}")
                            cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
            
            # Status display
            if blink_count < REQUIRED_BLINKS:
                status = f"Blink {REQUIRED_BLINKS - blink_count} more time(s)"
                color = (0, 255, 255)
            elif captured_frames < total_frames_needed:
                status = f"Capturing: {captured_frames}/{total_frames_needed}"
                color = (0, 255, 0)
            else:
                status = "Registration complete!"
                color = (0, 255, 0)
            
            cv2.putText(display_frame, status, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.putText(display_frame, f"EAR: {ear:.2f}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow('Face Registration - Press Q to cancel', display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            print("\nRegistration cancelled by user.")
            cap.release()
            cv2.destroyAllWindows()
            return False
        
        # Check if registration complete
        if captured_frames >= total_frames_needed:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if len(encodings) < total_frames_needed:
        print(f"\n✗ Registration failed - only captured {len(encodings)} images")
        return False
    
    print(f"\n✓ Successfully captured {len(encodings)} face encodings!")
    print(f"💾 Saving user data...")
    
    if save_user_encodings(username, encodings):
        print(f"✓ User '{username}' registered successfully!")
        print(f"✓ Data saved to: {USERS_DIR}/{username}.pickle")
        return True
    else:
        print(f"✗ Failed to save user data")
        return False


def recognize_faces():
    """
    Main recognition loop with motion detection and liveness verification.
    """
    print(f"\n{'='*60}")
    print("FACE RECOGNITION SYSTEM")
    print(f"{'='*60}")
    
    # Check for registered users
    registered_users = get_registered_users()
    if not registered_users:
        print("\n✗ No registered users found!")
        print("Register a user first with: python face_scanner.py --register username")
        return
    
    print(f"\n📋 Registered users: {', '.join(registered_users)}")
    
    # Initialize dlib
    detector = dlib.get_frontal_face_detector()
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    
    if not os.path.exists(predictor_path):
        print(f"\n⚠ Facial landmark predictor not found!")
        print(f"Please download from: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
        return
    
    predictor = dlib.shape_predictor(predictor_path)
    
    # Load all user encodings
    known_encodings = []
    known_names = []
    
    print("\n📂 Loading user encodings...")
    for username in registered_users:
        encodings = load_user_encodings(username)
        if encodings:
            known_encodings.extend(encodings)
            known_names.extend([username] * len(encodings))
            print(f"  ✓ Loaded {len(encodings)} encodings for {username}")
    
    if not known_encodings:
        print("\n✗ No valid encodings found!")
        return
    
    # Open webcam
    print("\n📷 Initializing webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Could not open webcam!")
        return
    
    print("✓ Webcam ready!")

    # Initialize ESP32
    esp32 = init_esp32()
    send_to_esp32(esp32, "READY")

    print("\nSYSTEM ACTIVE - Monitoring for motion...")
    print("Press 'q' to quit\n")

    # State variables
    prev_frame = None
    motion_cooldown = 0
    last_access_result = None
    access_display_end = 0
    
    # Liveness verification state
    verifying_liveness = False
    liveness_blink_count = 0
    liveness_eyes_closed = False
    liveness_username = None
    liveness_face_location = None
    liveness_start_time = 0
    LIVENESS_TIMEOUT = 5  # seconds
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to read from webcam")
            break
        
        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        display_frame = frame.copy()
        current_time = time.time()
        
        # Check if we're still displaying an access result
        if current_time < access_display_end and last_access_result:
            username, is_granted = last_access_result
            
            # Draw full-screen colored overlay
            overlay = display_frame.copy()
            color = (0, 255, 0) if is_granted else (0, 0, 255)
            cv2.rectangle(overlay, (0, 0), (display_frame.shape[1], display_frame.shape[0]), color, -1)
            cv2.addWeighted(overlay, 0.3, display_frame, 0.7, 0, display_frame)
            
            # Display result text
            text = f"ACCESS GRANTED: {username}" if is_granted else f"ACCESS DENIED: {username}"
            
            # Calculate text size and adjust if too large for screen
            font_scale = 1.0
            thickness = 2
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
            
            # If text is too wide, reduce font size
            max_width = display_frame.shape[1] * 0.9  # 90% of screen width
            if text_size[0] > max_width:
                font_scale = (max_width / text_size[0]) * font_scale
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
            
            text_x = (display_frame.shape[1] - text_size[0]) // 2
            text_y = display_frame.shape[0] // 2
            cv2.putText(display_frame, text, (text_x, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
            
            cv2.imshow('Face Recognition System - Press Q to quit', display_frame)
            if cv2.waitKey(1) & 0xFF in [ord('q'), ord('Q')]:
                break
            continue
        
        # Liveness verification mode
        if verifying_liveness:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray, 0)
            
            # Check timeout
            if current_time - liveness_start_time > LIVENESS_TIMEOUT:
                print("⏰ Liveness verification timed out")
                send_to_esp32(esp32, "DENIED:Timeout")
                verifying_liveness = False
                liveness_blink_count = 0
                motion_cooldown = 30
                last_access_result = ("Timeout", False)
                access_display_end = current_time + ACCESS_DISPLAY_TIME
                continue
            
            if len(faces) > 0:
                face = faces[0]
                shape = predictor(gray, face)
                shape_np = np.array([[shape.part(i).x, shape.part(i).y] for i in range(68)])
                
                left_eye = shape_np[LEFT_EYE_INDICES]
                right_eye = shape_np[RIGHT_EYE_INDICES]
                
                left_ear = calculate_eye_aspect_ratio(left_eye)
                right_ear = calculate_eye_aspect_ratio(right_eye)
                ear = (left_ear + right_ear) / 2.0
                
                # Blink detection
                if ear < EYE_AR_THRESHOLD:
                    if not liveness_eyes_closed:
                        liveness_eyes_closed = True
                else:
                    if liveness_eyes_closed:
                        liveness_blink_count += 1
                        print(f"   👁️  Blink detected! ({liveness_blink_count}/1)")
                        liveness_eyes_closed = False
                
                # Draw face rectangle
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                cv2.rectangle(display_frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                
                # Show instruction
                cv2.putText(display_frame, f"BLINK to verify ({liveness_blink_count}/1)", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                cv2.putText(display_frame, f"User: {liveness_username}", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Check if liveness verified
                if liveness_blink_count >= 1:
                    print(f"\n✓ ACCESS GRANTED: {liveness_username}")
                    print(f"  ✓ Liveness verified with blink")
                    send_to_esp32(esp32, f"GRANTED:{liveness_username}")
                    last_access_result = (liveness_username, True)
                    access_display_end = current_time + ACCESS_DISPLAY_TIME
                    verifying_liveness = False
                    liveness_blink_count = 0
                    motion_cooldown = 30
            else:
                cv2.putText(display_frame, "Face lost - look at camera", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            cv2.imshow('Face Recognition System - Press Q to quit', display_frame)
            if cv2.waitKey(1) & 0xFF in [ord('q'), ord('Q')]:
                break
            continue
        
        # Motion detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if prev_frame is None:
            prev_frame = gray
            continue
        
        # Calculate frame difference
        frame_delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_delta, MOTION_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) > MOTION_MIN_AREA:
                motion_detected = True
                break
        
        # Update previous frame
        prev_frame = gray.copy()
        
        # Handle motion cooldown
        if motion_cooldown > 0:
            motion_cooldown -= 1
            cv2.putText(display_frame, f"Cooldown: {motion_cooldown}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 2)
        elif motion_detected:
            print("\n🔔 Motion detected! Scanning for faces...")
            
            # Recognize faces
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            if len(face_encodings) > 0:
                print(f"   Found {len(face_encodings)} face(s)")
                
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    # Compare with known faces
                    matches = face_recognition.compare_faces(known_encodings, face_encoding, 
                                                            tolerance=RECOGNITION_TOLERANCE)
                    face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                    
                    cv2.rectangle(display_frame, (left, top), (right, bottom), (255, 255, 0), 2)
                    
                    if True in matches:
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            username = known_names[best_match_index]
                            confidence = 1 - face_distances[best_match_index]
                            
                            if confidence >= MIN_CONFIDENCE:
                                print(f"   Matched: {username} (confidence: {confidence:.2%})")
                                print(f"   👁️  Verifying liveness - please BLINK...")
                                
                                # Start liveness verification
                                verifying_liveness = True
                                liveness_blink_count = 0
                                liveness_eyes_closed = False
                                liveness_username = username
                                liveness_face_location = (top, right, bottom, left)
                                liveness_start_time = current_time
                            else:
                                print(f"   Low confidence: {username} ({confidence:.2%})")
                                send_to_esp32(esp32, "DENIED:Low Conf")
                                last_access_result = ("Low Confidence", False)
                                access_display_end = current_time + ACCESS_DISPLAY_TIME
                                motion_cooldown = 30
                    else:
                        print("   No match found - unknown face")
                        send_to_esp32(esp32, "DENIED:Unknown")
                        last_access_result = ("Unknown", False)
                        access_display_end = current_time + ACCESS_DISPLAY_TIME
                        motion_cooldown = 30
            else:
                print("   No faces detected")
                motion_cooldown = 10
        else:
            # No motion - show idle status
            cv2.putText(display_frame, "Monitoring for motion...", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.imshow('Face Recognition System - Press Q to quit', display_frame)
        
        if cv2.waitKey(1) & 0xFF in [ord('q'), ord('Q')]:
            print("\n👋 Shutting down face recognition system...")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    if esp32 and esp32.is_open:
        send_to_esp32(esp32, "OFFLINE")
        esp32.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Face Scanner - Registration and Recognition System')
    parser.add_argument('--register', type=str, metavar='USERNAME',
                       help='Register a new user with the given username')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("        FACE SCANNER - Recognition System")
    print("="*60)
    
    try:
        if args.register:
            register_user(args.register)
        else:
            recognize_faces()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

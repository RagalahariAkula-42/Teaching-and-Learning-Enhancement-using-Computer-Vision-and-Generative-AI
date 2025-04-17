import os
import numpy as np
import cv2
import math
import mediapipe as mp
import HandTrackingModule as htm
import subprocess
import sounddevice as sd
import pygetwindow as gw

# FFmpeg recording setup
output_file = "D:/output.avi"  # Output file for the recording
ffmpeg_process = None

def get_active_microphone():
    """Detect the active microphone dynamically."""
    # Set the exact name detected for your audio device
    microphone_name = "Microphone Array (Intel® Smart Sound Technology for Digital Microphones)"
    
    # Ensure it's available for FFmpeg
    devices = sd.query_devices()
    for device in devices:
        if device['name'] == microphone_name and device['max_input_channels'] > 0:
            print(f"Using microphone: {microphone_name}")
            return microphone_name
    raise RuntimeError("No active microphone detected.")


def start_ffmpeg_recording(microphone_name):
    global ffmpeg_process
    command = [
        "./FFmpeg/bin/ffmpeg.exe",
        "-y",  # Overwrite output file if it exists
        "-f", "gdigrab",  # Screen capture input for Windows (use 'x11grab' for Linux)
        "-framerate", "30",  # Frame rate
        "-i", "desktop",  # Capture the entire desktop
        "-f", "dshow",  # Audio input
        "-i", f"audio={microphone_name}",  # Use the detected microphone
        "-c:v", "libx264",  # Video codec
        "-preset", "ultrafast",  # Encoding speed
        "-crf", "23",  # Quality (lower is better, 23 is default)
        "-c:a", "aac",  # Audio codec
        "-b:a", "192k",  # Audio bitrate
        "-probesize", "5000000",  # Increase probesize (5MB)
        "-analyzeduration", "5000000",  # Increase analyzeduration (5MB)
        output_file  # Output file
    ]
    ffmpeg_process = subprocess.Popen(command, stdin=subprocess.PIPE)
    print("Screen and audio recording started.")


def stop_ffmpeg_recording():
    """Stop FFmpeg recording."""
    global ffmpeg_process
    if ffmpeg_process:
        ffmpeg_process.terminate()  # Safely terminate the process
        ffmpeg_process.wait()
        print(f"Recording saved to {output_file}")
        

# Initialize variables
color = "White"
drawColor = (255, 255, 255)
l, c, r, t = 0, 0, 0, 0
brushThickness = 10
eraserThickness = 30
shape = "Draw"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (255, 255, 255)
font_thickness = 2
text_position_color = (10, 80)
text_position_shape = (10, 120)

def load_image(image_path):
    """Load an image from the given path."""
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # Load image with alpha channel if present
    if img is None:
        print(f"Error: Unable to load image from path '{image_path}'")
    return img

# Load images
bin = load_image("./images/Bin.png")
colors = load_image("./images/Colors.png")
shapes = load_image("./images/Shapes.png")

mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.HandDetector(detectionCon=0.85)
(xq, yq) = (0, 0)
(xp, yp) = (0, 0)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

# Detect the active microphone and start FFmpeg recording
try:
    microphone_name = get_active_microphone()
    start_ffmpeg_recording(microphone_name)
except RuntimeError as e:
    print(e)
    cap.release()
    cv2.destroyAllWindows()
    exit()

cv2.namedWindow("Virtual Painter", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Virtual Painter", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)

    results = selfie_segmentation.process(img)
    condition = results.segmentation_mask > 0.5

    black_screen = np.zeros_like(img)
    output_image = black_screen

    if len(lmlist[0]) != 0:
        lmlist_new = lmlist[0]
        x1, y1 = lmlist_new[8][1:]
        x2, y2 = lmlist_new[12][1:]
        x0, y0 = lmlist_new[4][1:]
        x4, y4 = lmlist_new[20][1:]

        fingers = detector.fingersUp()

        if fingers[1] and fingers[2]:  # Selection Mode
            (xp, yp) = (0, 0)
            (xq, yq) = (0, 0)
            if y1 < 60:
                if 0 <= x1 < 100:
                    drawColor = (0, 0, 255)
                    color = "Red"
                elif 100 <= x1 < 200:
                    drawColor = (255, 0, 0)
                    color = "Blue"
                elif 200 <= x1 < 300:
                    drawColor = (0, 255, 0)
                    color = "Green"
                elif 300 <= x1 < 400:
                    drawColor = (0, 255, 255)
                    color = "Yellow"
                elif 400 <= x1 < 500:
                    drawColor = (255, 255, 255)
                    color = "White"
                elif 500 <= x1 < 600:
                    shape = "Draw"
                elif 600 <= x1 < 700:
                    shape = "Line"
                    l = 0
                elif 700 <= x1 < 800:
                    shape = "Circle"
                    c = 0
                elif 800 <= x1 < 900:
                    shape = "Rectangle"
                    r = 0
                elif 900 <= x1 < 1000:
                    shape = "Triangle"
                    t = 0
                elif 1000 <= x1 < 1100:
                    shape = "Erase"
                    color = "---"
                    drawColor = (169, 169, 169)
                elif 1100 <= x1 < 1200:
                    imgCanvas = np.zeros((720, 1280, 3), np.uint8)
            cv2.rectangle(output_image, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        if fingers[1] and fingers[2] == False and fingers[0] == False:  # Drawing Mode
            cv2.circle(output_image, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
                
            if drawColor == (169, 169, 169):  # Erasing
                cv2.line(output_image, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), (0,0,0), eraserThickness)

            elif shape == "Draw":  # Drawing
                cv2.line(output_image, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1
        
        if fingers[0] and fingers[1] and fingers[2] == False:  # Shape Mode
            if shape == "Line":
                cv2.line(output_image, (x0, y0), (x1, y1), drawColor, brushThickness)
            elif shape == "Circle":
                radius = int(math.sqrt((x0 - x0)**2 + (y1 - yq)**2))
                cv2.circle(output_image, (x0, y0), radius, drawColor, brushThickness)
            elif shape == "Rectangle":
                cv2.rectangle(output_image, (x0, y0), (x1, y1), drawColor, brushThickness)
            elif shape == "Triangle":
                pts = np.array([[x0, y0], [x1, y1], [x1, y0]], np.int32)
                cv2.polylines(output_image, [pts], isClosed=True, color=drawColor, thickness=brushThickness)

            if fingers[4]:
                xq, yq = x0, y0
                if shape == "Line":
                    if l == 0:
                        cv2.line(output_image, (xq, yq), (x1, y1), drawColor, brushThickness)
                        cv2.line(imgCanvas, (xq, yq), (x1, y1), drawColor, brushThickness)

                    l = 1
                    shape = "Draw"
                elif shape == "Circle":
                    if c == 0:
                        radius = int(math.sqrt((x1 - xq)**2 + (y1 - yq)**2))
                        cv2.circle(output_image, (xq, yq), radius, drawColor, brushThickness)
                        cv2.circle(imgCanvas, (xq, yq), radius, drawColor, brushThickness)

                    c = 1
                    shape = "Draw"
                elif shape == "Rectangle":
                    if r == 0:
                        cv2.rectangle(output_image, (xq, yq), (x1, y1), drawColor, brushThickness)
                        cv2.rectangle(imgCanvas, (xq, yq), (x1, y1), drawColor, brushThickness)

                    r = 1
                    shape = "Draw"
                elif shape == "Triangle":
                    if t == 0:
                        pts = np.array([[x0, y0], [x1, y1], [x1, y0]], np.int32)
                        cv2.polylines(output_image, [pts], isClosed=True, color=drawColor, thickness=brushThickness)
                        cv2.polylines(imgCanvas, [pts], isClosed=True, color=drawColor, thickness=brushThickness)
                    t = 1
                    shape = "Draw"
                    

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(output_image, imgInv)
    img = cv2.bitwise_or(output_image, imgCanvas)

    # Display color and shape information
    cv2.putText(img, f"Color: {color}", text_position_color, font, font_scale, font_color, font_thickness)
    cv2.putText(img, f"Shape: {shape}", text_position_shape, font, font_scale, font_color, font_thickness)

    img[0:60, 0:500] = colors
    img[0:60, 500:1100] = shapes
    img[0:60, 1100:1200] = bin

    # Capture the camera feed
    success, person_feed = cap.read()
    if success:
        person_feed = cv2.flip(person_feed, 1)  # Flip horizontally for a mirror effect
        
        # Apply hand detection to the camera feed
        person_feed = detector.findHands(person_feed)
        
        # Resize the camera feed
        person_feed_resized = cv2.resize(person_feed, (200, 150))  # Resize to smaller window

        # Overlay the resized camera feed with hand detection onto the main frame
        img[570:720, 1080:1280] = person_feed_resized
    
    cv2.imshow("Virtual Painter", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop FFmpeg recording and release resources
stop_ffmpeg_recording()
cap.release()
cv2.destroyAllWindows()

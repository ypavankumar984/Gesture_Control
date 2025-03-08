import cv2
import mediapipe as mp
import pyautogui
import time
import keyboard

# Initialize MediaPipe hands and PyAutoGUI
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Camera setup
cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

# Screen dimensions (for pyautogui)
screenWidth, screenHeight = pyautogui.size()

# Smoothing factor to avoid jitter
smoothening = 5
prevX, prevY = 0, 0
currX, currY = 0, 0

# Time tracking for FPS calculation
pTime = 0

# Previous distance for zoom tracking
prevDistance = 0
zoomCooldown = 1.5  # Cooldown to prevent excessive zooming
lastZoomTime = 0

while True:
    # Read frame from the camera
    success, img = cap.read()
    if not success:
        break
    
    # Convert the image to RGB (for MediaPipe processing)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the image
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get finger tip positions
            indexFinger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            middleFinger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            
            x1, y1 = int(indexFinger.x * wCam), int(indexFinger.y * hCam)
            x2, y2 = int(thumb.x * wCam), int(thumb.y * hCam)
            x3, y3 = int(middleFinger.x * wCam), int(middleFinger.y * hCam)
            
            # Map coordinates to screen size (invert x for natural movement)
            mappedX = screenWidth - (x1 * screenWidth // wCam)
            mappedY = y1 * screenHeight // hCam
            
            # Smooth movement
            currX = prevX + (mappedX - prevX) // smoothening
            currY = prevY + (mappedY - prevY) // smoothening
            
            # Move mouse
            pyautogui.moveTo(currX, currY, duration=0.1)
            prevX, prevY = currX, currY
            
            # Draw a circle on the finger position
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            
            # Click logic: Index & Middle Finger Tap
            clickDistance = ((x3 - x1) ** 2 + (y3 - y1) ** 2) ** 0.5
            if clickDistance < 30:  # Close enough to be a tap
                pyautogui.click()
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                time.sleep(0.2)  # Delay to prevent multiple clicks
            
            # Zoom logic: Pinch Gesture (Index & Thumb)
            zoomDistance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            currentTime = time.time()
            if currentTime - lastZoomTime > zoomCooldown:
                if zoomDistance < 80 and prevDistance - zoomDistance > 10:
                    keyboard.press_and_release('ctrl+-')  # Zoom Out
                    lastZoomTime = currentTime
                elif zoomDistance > prevDistance + 15:
                    keyboard.press_and_release('ctrl+=')  # Zoom In
                    lastZoomTime = currentTime
            
            prevDistance = zoomDistance
    
    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime
    
    # Display FPS
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    
    cv2.namedWindow("Virtual Mouse", cv2.WINDOW_NORMAL)  # Make window resizable
    cv2.resizeWindow("Virtual Mouse", 950, 1200)  # Set width and height
    cv2.imshow("Virtual Mouse", img)

    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()

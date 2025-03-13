

import numpy as np
import cv2

DROIDCAM_IP = "192.168.8.102"  # Replace with your phone's IP
VIDEO_URL = f"http://{DROIDCAM_IP}:4747/video"

cap = cv2.VideoCapture(VIDEO_URL)

canvas = np.zeros((480, 640, 3), dtype=np.uint8)
center_points_blue = []
center_points_red = []
x, y, w, h = 100, 50, 150, 100

# Track which color is currently active
active_color = None

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to capture frame. Check DroidCam connection.")
        break
    
    frame = cv2.resize(frame, (640, 480))
    
    # Get ROI for color detection
    roi = frame[y:y+h, x:x+w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Convert full frame to HSV for tracking
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define color ranges
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    lower_red1 = np.array([0, 150, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 150, 50])
    upper_red2 = np.array([180, 255, 255])
    
    # Check ROI for colors
    mask_red1_roi = cv2.inRange(hsv_roi, lower_red1, upper_red1)
    mask_red2_roi = cv2.inRange(hsv_roi, lower_red2, upper_red2)
    mask_red_roi = cv2.bitwise_or(mask_red1_roi, mask_red2_roi)
    mask_blue_roi = cv2.inRange(hsv_roi, lower_blue, upper_blue)
    
    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask_blue_roi = cv2.morphologyEx(mask_blue_roi, cv2.MORPH_OPEN, kernel)
    mask_blue_roi = cv2.morphologyEx(mask_blue_roi, cv2.MORPH_CLOSE, kernel)
    mask_red_roi = cv2.morphologyEx(mask_red_roi, cv2.MORPH_OPEN, kernel)
    mask_red_roi = cv2.morphologyEx(mask_red_roi, cv2.MORPH_CLOSE, kernel)
    
    # Determine active color from ROI
    if cv2.countNonZero(mask_blue_roi) > 500:
        active_color = "blue"
    elif cv2.countNonZero(mask_red_roi) > 500:
        active_color = "red"
    
    # Track the active color in the full frame
    if active_color == "blue":
        mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue
            
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                center_points_blue.append((cX, cY))
                
                # Draw a circle at the current position
                cv2.circle(frame, (cX, cY), 5, (255, 0, 0), -1)
    
    elif active_color == "red":
        mask_red1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask_red1, mask_red2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue
            
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                center_points_red.append((cX, cY))
                
                # Draw a circle at the current position
                cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
    
    # Draw the lines on canvas and frame
    if len(center_points_blue) > 1:
        for i in range(1, len(center_points_blue)):
            cv2.line(canvas, center_points_blue[i-1], center_points_blue[i], (255, 0, 0), 4)
            cv2.line(frame, center_points_blue[i-1], center_points_blue[i], (255, 0, 0), 4)
    
    if len(center_points_red) > 1:
        for i in range(1, len(center_points_red)):
            cv2.line(canvas, center_points_red[i-1], center_points_red[i], (0, 0, 255), 4)
            cv2.line(frame, center_points_red[i-1], center_points_red[i], (0, 0, 255), 4)
    
    # Draw the ROI rectangle
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Display the active color
    cv2.putText(frame, f"Active Color: {active_color}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Show the frames
    cv2.imshow("Canvas", canvas)
    cv2.imshow("DroidCam Feed", frame)
    
    if active_color == "blue":
        cv2.imshow("Active Color Mask", mask)
    elif active_color == "red":
        cv2.imshow("Active Color Mask", mask)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import numpy as np
import cv2


DROIDCAM_IP = "192.168.8.102"  # Replace with your phone's IP
VIDEO_URL = f"http://{DROIDCAM_IP}:4747/video"


cap = cv2.VideoCapture(VIDEO_URL)


canvas = np.zeros((480, 640, 3), dtype=np.uint8)
center_points_blue = []
center_points_red = []

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Check DroidCam connection.")
        break
    
    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    lower_red1 = np.array([0, 150, 50])   
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 150, 50])  
    upper_red2 = np.array([180, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

    
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    
    kernel = np.ones((5, 5), np.uint8)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)  
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_CLOSE, kernel)  
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel) 
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
    
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours_blue:
        
        if cv2.contourArea(contour) < 500:  
            continue

        
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX_blue = int(M["m10"] / M["m00"])
            cY_blue = int(M["m01"] / M["m00"])
            center_points_blue.append((cX_blue, cY_blue))
    for contour in contours_red:
        
        if cv2.contourArea(contour) < 500:  
            continue

        
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX_red = int(M["m10"] / M["m00"])
            cY_red = int(M["m01"] / M["m00"])
            center_points_red.append((cX_red, cY_red))
            

    
    for i in range(1, len(center_points_blue)):
        cv2.line(canvas, center_points_blue[i - 1], center_points_blue[i], (255, 0, 0), 4)
        cv2.line(frame, center_points_blue[i - 1], center_points_blue[i], (255, 0, 0), 4)
    for i in range(1, len(center_points_red)):
        cv2.line(canvas, center_points_red[i - 1], center_points_red[i], (0, 0,255), 4)
        cv2.line(frame, center_points_red[i - 1], center_points_red[i], (0, 0, 255), 4)
    
    cv2.imshow("Canvas", canvas)
    cv2.imshow("Filtered Mask", mask_blue)
    cv2.imshow("DroidCam Feed", frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

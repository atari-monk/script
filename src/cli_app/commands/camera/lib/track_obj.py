#pip install opencv-python opencv-python-headless numpy

import cv2
import numpy as np

# Initialize the webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

# Define the range of color to track (e.g., green in HSV)
# You can change these values to track a different color
lower_color = np.array([35, 50, 50])  # Lower bound of green color in HSV
upper_color = np.array([85, 255, 255])  # Upper bound of green color in HSV

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    # Convert the frame to HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask to detect the object
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Perform morphological operations to remove small noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # If we found any contours, proceed with tracking
    if contours:
        # Sort contours by area and get the largest one
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Draw the bounding box on the original frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Optional: Draw the center of the object
        center = (x + w // 2, y + h // 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
    
    # Display the frame with the tracked object
    cv2.imshow("Object Tracking", frame)
    
    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()

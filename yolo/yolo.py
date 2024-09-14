import cv2
import numpy as np
from cvzone.FaceMeshModule import FaceMeshDetector  # Replace with actual distance calculation if needed
from ultralytics import YOLO  # Ensure YOLO model is imported

# Load YOLO model
model = YOLO("yolov8m.pt")  # Adjust to your model's path

# Initialize video capture and object detection
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Error opening camera"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Initialize video writer (optional, if you want to save the video)
video_writer = cv2.VideoWriter("object_detection_distance.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Initialize distance-calculation parameters
# The following are example values; you should adjust them based on your setup
object_real_width = 20.0  # Real width of the object in cm
focal_length = 840        # Focal length of the camera (example value)

while True:
    success, im0 = cap.read()
    if not success:
        print("Failed to grab frame or camera feed has ended.")
        break

    # Perform object detection with YOLO
    results = model.predict(im0)
    detections = results[0].boxes

    # Process detected objects
    for box in detections:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        class_id = int(box.cls[0].item())
        prob = round(box.conf[0].item(), 2)
        label = model.names[class_id]
        
        # Calculate object width in pixels
        object_width_pixels = x2 - x1
        
        # Calculate distance
        if object_width_pixels > 0:
            distance = (object_real_width * focal_length) / object_width_pixels
            print(f'Distance: {distance:.2f} cm')
            cv2.putText(im0, f'Distance of {label}: {int(distance)}  cm', 
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Draw bounding box and label
        cv2.rectangle(im0, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(im0, f'Probability:  {prob:.2f}% {label}   ', 
                    (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Display the frame
    cv2.imshow("Camera Feed", im0)
    
    # Optional: Write the frame to video file
    video_writer.write(im0)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
video_writer.release()
cv2.destroyAllWindows()

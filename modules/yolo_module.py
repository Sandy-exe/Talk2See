from ultralytics import YOLO

# Load YOLO model
model = YOLO("Required_Files/yolov8m.pt")  # Adjust to your model's path
object_real_width = 20.0  # Real width of the object in cm
focal_length = 840        # Focal length of the camera (example value)

def yolo_object_detection(image):
    try:
        results = model.predict(image)
        detections = results[0].boxes
        DETECTIONS = ''
        for box in detections:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            class_id = int(box.cls[0].item())
            prob = round(box.conf[0].item(), 2)
            label = model.names[class_id]
            object_width_pixels = x2 - x1

            if object_width_pixels > 0 and prob > 0.5:
                distance = (object_real_width * focal_length) / object_width_pixels
                DETECTIONS += f'Distance of {label}: {distance:.2f} cm\n'
        return DETECTIONS
    except Exception as e:
        print(f"Error in YOLO detection: {e}")
        return "Error"

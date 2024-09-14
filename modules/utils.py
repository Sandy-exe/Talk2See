import cv2
import threading

stop_event = threading.Event()

def is_blurry(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    return fm < 50, fm  # Adjust the threshold as needed

def stop_threads():
    global stop_event
    stop_event.set()

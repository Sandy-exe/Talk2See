import cv2
import threading
from modules.yolo_module import yolo_object_detection
from modules.ocr_module import get_OCR
from modules.image_captioning import query_image_captioning
from modules.gpt_module import chatgpt_api
from modules.tts_module import speak
from modules.utils import is_blurry, stop_threads

def process_frame_with_threads(frame):
    try:
        global speak_thread_running

        # Shared variables to hold the results from each thread
        yolo_result = [None]
        ocr_result = [None]
        caption_result = [None]

        # YOLO detection thread
        def yolo_thread():
            yolo_result[0] = yolo_object_detection(frame)

        # OCR thread
        def ocr_thread():
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ocr_result[0] = get_OCR(gray)

        # Image Captioning thread
        def caption_thread():
            cv2.imwrite('temp_image.jpg', frame)
            caption_output = query_image_captioning('temp_image.jpg')
            if isinstance(caption_output, list) and 'generated_text' in caption_output[0]:
                caption_result[0] = caption_output[0]['generated_text']
            else:
                caption_result[0] = "Error"

        # Create and start the threads
        threads = []
        threads.append(threading.Thread(target=yolo_thread))
        threads.append(threading.Thread(target=ocr_thread))
        threads.append(threading.Thread(target=caption_thread))

        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check if all threads resulted in errors
        if yolo_result[0] == "Error" and ocr_result[0] == "Error" and caption_result[0] == "Error":
            chatgpt_response = "Threads not working"
        else:
            # Combine results
            combined_text = f"YOLO Detection: {yolo_result[0]}\nOCR: {ocr_result[0]}\nCaption: {caption_result[0]}"
            
            print("Combined Text:", combined_text)
            # Send to ChatGPT for final processing
            chatgpt_response = chatgpt_api(combined_text)
        
        # Speak the final response
        if not speak_thread_running:
            speak_thread = threading.Thread(target=speak, args=(chatgpt_response,))
            speak_thread.start()
            speak_thread_running = True
            
        return chatgpt_response
        
    except Exception as e:
        print(f"Error in process_frame_with_threads: {e}")
        return "Error"
    

def main():
    cap = cv2.VideoCapture(0)
    assert cap.isOpened(), "Error opening camera"

    global speak_thread_running
    speak_thread_running = False
    
    global image_processing
    image_processing = False

    def process_frame_thread(frame):
        response = process_frame_with_threads(frame)
        global image_processing
        image_processing = False
        print("Response:", response)
        

    while cap.isOpened():
        active_threads = threading.enumerate()
        if active_threads:
            print(f"Active threads: {[thread.name for thread in active_threads]}")

        ret, frame = cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            break

        # Process frame using threads for YOLO, OCR, and Image Captioning
        if not is_blurry(frame)[0] and not image_processing:
            print("Processing frame...")
            image_processing = True
            thread = threading.Thread(target=process_frame_thread, args=(frame,))
            thread.start()
        
        # Display the frame
        if image_processing:
            cv2.putText(frame, "Processing...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif is_blurry(frame):
            cv2.putText(frame, "Image is Blurry", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Press 'q' to exit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        cv2.imshow('Camera Feed', frame)
        
        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

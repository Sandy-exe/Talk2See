import cv2
import threading
import time
from modules.yolo_module import yolo_object_detection
from modules.ocr_module import get_OCR
from modules.image_captioning import query_image_captioning
from modules.gpt_module import chatgpt_api
from modules.tts_module import speak
from modules.utils import is_blurry, stop_threads
from modules.voice_module import listen_for_voice  # Assumed module for voice input

# Shared variables
latest_clear_frame = [None]  # Holds the latest clear frame for reuse if needed
speak_thread_running = False
image_processing = False
# Flag for interrupting processing when voice input is detected
voice_input_detected = False

# Lock for synchronized access
frame_lock = threading.Lock()


def process_frame_with_threads(frame):
    global speak_thread_running, image_processing, voice_input_detected

    try:
        # Variables to hold results from each thread
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

        # Wait for all threads to complete or exit if voice input detected
        for thread in threads:
            thread.join()
            if voice_input_detected:
                return "Voice input detected. Prioritizing voice command."

        # Combine results if no interruptions
        if yolo_result[0] == "Error" and ocr_result[0] == "Error" and caption_result[0] == "Error":
            chatgpt_response = "Threads not working"
        else:
            combined_text = f"YOLO Detection: {yolo_result[0]}\nOCR: {
                ocr_result[0]}\nCaption: {caption_result[0]}"
            chatgpt_response = chatgpt_api(combined_text)

        # Speak the final response if no interruption
        if not speak_thread_running:
            speak_thread = threading.Thread(
                target=speak, args=(chatgpt_response,))
            speak_thread.start()
            speak_thread_running = True

        return chatgpt_response

    except Exception as e:
        print(f"Error in process_frame_with_threads: {e}")
        return "Error"


def voice_input_thread():
    global voice_input_detected, latest_clear_frame, image_processing

    while True:
        # Listen for voice input (this function should block until a voice command is detected)
        voice_command = listen_for_voice()
        if voice_command:
            # Signal to prioritize voice command
            voice_input_detected = True

            # Process the latest clear frame with voice input as priority
            with frame_lock:
                if latest_clear_frame[0] is not None:
                    response = process_frame_with_threads(
                        latest_clear_frame[0])
                    print("Voice Triggered Response:", response)

            # Reset flags after processing
            voice_input_detected = False
            image_processing = False
            time.sleep(1)  # Prevent immediate retrigger


def main():
    cap = cv2.VideoCapture(0)
    assert cap.isOpened(), "Error opening camera"

    global image_processing, latest_clear_frame

    # Start voice input thread
    threading.Thread(target=voice_input_thread, daemon=True).start()

    def process_frame_thread(frame):
        response = process_frame_with_threads(frame)
        global image_processing
        image_processing = False
        print("Response:", response)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            break

        if not is_blurry(frame)[0] and not image_processing and not voice_input_detected:
            print("Processing frame...")
            image_processing = True
            # Update latest clear frame
            with frame_lock:
                latest_clear_frame[0] = frame.copy()

            # Start a new thread to process the frame
            thread = threading.Thread(
                target=process_frame_thread, args=(frame,))
            thread.start()

        # Display camera feed
        display_text = "Processing..." if image_processing else "Press 'q' to exit"
        if is_blurry(frame):
            display_text = "Image is Blurry"
        cv2.putText(frame, display_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Camera Feed', frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

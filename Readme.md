# Talk2See

**Talk2See** is an assistive technology project designed to help visually impaired individuals by providing spoken feedback about their surroundings. The system uses computer vision and AI models to analyze camera input and deliver descriptive audio feedback.

## Project Components

1. **YOLO Object Detection**: Detects objects in the camera feed and estimates their distance.
2. **OCR (Optical Character Recognition)**: Extracts text from images.
3. **Image Captioning**: Generates descriptive captions for the images.
4. **ChatGPT Integration**: Processes the collected data to provide clear and concise spoken feedback.
5. **Text-to-Speech (TTS)**: Converts the processed text into spoken words.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Sandy-exe/Talk2See.git
    cd Talk2See
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the main application**:
    ```bash
    python main.py
    ```

2. The application will start the camera feed and continuously process frames. It will provide feedback through text-to-speech based on the analysis of the camera input.

## File Structure

- `main.py`: The main entry point of the application, handles the camera feed and threading.
- `modules/yolo_module.py`: Contains YOLO object detection logic.
- `modules/ocr_module.py`: Handles OCR using Tesseract.
- `modules/image_captioning.py`: Manages image captioning via the Hugging Face API.
- `modules/gpt_module.py`: Integrates with OpenAI's ChatGPT.
- `modules/tts_module.py`: Manages text-to-speech functionality.
- `modules/utils.py`: Utility functions like blur detection and thread management.
- `requirements.txt`: Lists required Python packages.

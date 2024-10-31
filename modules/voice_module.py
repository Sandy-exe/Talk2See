import speech_recognition as sr

def listen_for_voice():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        # Use the microphone as the audio source
        with microphone as source:
            print("Listening for voice input...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)  # Adjust timeout as needed

        # Recognize the voice input
        voice_text = recognizer.recognize_google(audio)
        print("Voice input detected:", voice_text)
        return voice_text

    except sr.WaitTimeoutError:
        print("Listening timed out, no voice input detected.")
        return None
    except sr.UnknownValueError:
        print("Could not understand the voice input.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from the speech recognition service; {e}")
        return None

import speech_recognition as sr
import pygame
r = sr.Recognizer()

def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                print("speak")
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                return MyText
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        
        except sr.UnknownValueError:
            print("Unknown error occurred") 

def output_text(text):
    with open("output.txt", "a") as f:
        f.write(text + '\n')

# while True:
print("Listening....")
text = record_text()
# print(text)
# output_text(text)
    
#AI enabled

import openai

# Set your OpenAI API key
directions = '''from kitchen to hall u can go:
take left turn
go straight
take a right turn
reached kitchen
the kitchen is vice versa
'''
openai.api_key = "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"
messages = ""
def chatgpt_api(input_text):
    global messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant, who guides the user however he wants and store these directions so that u can guide the user whenever he asks alone"+directions}]

    if input_text:
        messages.append(
            {"role": "user", "content": ""+input_text},
        )
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat_completion.choices[0].message.content
    # messages.append()
    # print(chat_completion.choices[0].message)
    return reply

user_input = text
print(user_input)
response = chatgpt_api(user_input)
print("ChatGPT:", response)


from gtts import gTTS
import pygame
from io import BytesIO
import tempfile
import os

def text_to_speech(text):
    # Create a gTTS object
    tts = gTTS(text=text, lang='en', slow=False)  # Adjust language and speed as needed

    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        tts.write_to_fp(temp_audio)

        # Close the file to ensure it's fully written to disk
        temp_audio.close()

        # Play the audio using pygame
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio.name)
        pygame.mixer.music.play()

        # Wait until the speech finishes playing
        while pygame.mixer.music.get_busy():
            continue

        # Stop the mixer
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    # Delete the temporary file
    os.unlink(temp_audio.name)

# Example usage
text_to_speech(response)






import pyttsx3

engine = pyttsx3.init()

def speak(text):
    try: 
        if text == "Error":
            engine.say("Sorry, I am unable to process the information at the moment. Please try again later.")
            engine.runAndWait()
            return
        
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(e)

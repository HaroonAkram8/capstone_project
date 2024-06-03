import speech_recognition as sr

def speech_to_text() -> str:
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Awaiting instructions...")
        audio = r.listen(source)

        try:   
            query = r.recognize_google(audio, language='en-US')
            print(f"User: {query}\n")

            return query

        except Exception:
            print("Did not catch that\n")
    
    return None
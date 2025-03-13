import speech_recognition as sr

def speech_to_text() -> str:
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source=source, duration=1)

        print("Awaiting spoken instructions...")
        audio = r.listen(source)

        try:   
            query = r.recognize_google(audio, language='en-US')
            print(f"User: {query}\n")

            return query

        except Exception:
            print("Did not catch that\n")
    
    return None

# Example usage
if __name__ == "__main__":
    query = speech_to_text()
    print(query)

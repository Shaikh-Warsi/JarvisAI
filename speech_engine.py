import speech_recognition as sr
import task_manager
import predefined_tasks
import asyncio

async def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("🎙️ Listening... Speak now.")

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = await asyncio.to_thread(recognizer.listen, source)
        command = recognizer.recognize_google(audio).lower()
        print(f"🗣️ You said: {command}")
        return command
    except sr.UnknownValueError:
        print("❌ Sorry, couldn't understand. Try again.")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

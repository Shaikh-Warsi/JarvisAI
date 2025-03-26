import sounddevice as sd
import queue
import json
import vosk
import threading

# Load Vosk Model
MODEL_PATH = "vosk_model"
samplerate = 16000
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, samplerate)
audio_queue = queue.Queue(maxsize=50)  # ✅ Prevents memory overflow
stop_event = threading.Event()

vosk.SetLogLevel(0)  # ✅ Reduce unnecessary logs

def callback(indata, frames, time, status):
    """Continuously stream audio into the queue."""
    if status:
        print(f"🎤 Audio status: {status}")
    
    try:
        if audio_queue.full():
            audio_queue.get_nowait()  # ✅ Remove the oldest packet (prevents data loss)
        audio_queue.put_nowait(bytes(indata))  # ✅ Non-blocking put
    except queue.Full:
        print("⚠️ Audio queue is full! Dropping old packets.")

def listen():
    """Listens for speech and returns the transcribed text."""
    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize=4000, dtype='int16',
                               channels=1, callback=callback):
            print("🎙️ Listening... Speak now.")
            
            final_text = ""
            partial_text = ""
            
            while not stop_event.is_set():
                try:
                    data = audio_queue.get(timeout=1)  # ✅ Prevents indefinite blocking
                except queue.Empty:
                    continue
                
                if recognizer.AcceptWaveform(data):
                    try:
                        result = json.loads(recognizer.Result())
                        final_text = result.get("text", "").strip()
                        if final_text:
                            print(f"✅ Final Speech: {final_text}")
                            return final_text
                    except json.JSONDecodeError:
                        print("⚠️ Error decoding JSON from Vosk.")
                else:
                    try:
                        partial_result = json.loads(recognizer.PartialResult())
                        partial_text = partial_result.get("partial", "").strip()
                        if partial_text:
                            print(f"🟡 Partial Speech: {partial_text}")
                    except json.JSONDecodeError:
                        print("⚠️ Error decoding partial JSON.")
            
            return final_text or partial_text  # ✅ Ensures partial speech is not lost

    except Exception as e:
        print(f"❌ Microphone error: {e}")
        return None

def stop_listening():
    """Stops the listening loop gracefully."""
    stop_event.set()

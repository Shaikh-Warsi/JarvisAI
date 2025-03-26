# JarvisAI

# 🎙️ AI-Powered Task Automation Assistant 🚀

**An advanced AI-powered voice assistant** that listens to voice commands, evaluates the task, generates the appropriate Python code, and automatically executes it. Powered by **Google Gemini-2.0-Flash** for intelligent code generation and task handling.

---

## 🔥 **Features**

✅ Voice recognition using `speech_recognition`  
✅ AI-powered task evaluation and Python code generation using `Google Gemini`  
✅ Automatic execution of generated code  
✅ Real-time speech feedback with `pyttsx3`  
✅ Error handling and feedback  

---

## 📂 **Project Structure**

```plaintext
📁 Assistant Stage 1
 ├── ai_engine.py        # Handles interaction with Google Gemini AI
 ├── config.py           # API key configuration
 ├── gui.py              # GUI interface (if applicable)
 ├── main.py             # Main entry point to run the assistant
 ├── speech_engine.py    # Handles speech recognition
 ├── task_manager.py     # Manages task execution
 ├── generated_task.py   # Stores generated code temporarily
 ├── README.md           # Project documentation
 └── requirements.txt    # Python dependencies


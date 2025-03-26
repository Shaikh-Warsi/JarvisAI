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


⚙️ Setup Instructions
1️⃣ Clone the repository
bash
Copy
Edit
git clone https://github.com/your-username/ai-task-assistant.git
cd ai-task-assistant
2️⃣ Install Dependencies
Install the required Python packages.

bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Set Up Google Gemini API
Go to Google AI Studio

Generate your API key.

Add it to the config.py file:

python
Copy
Edit
# /config.py
GEMINI_API_KEY = "YOUR_GOOGLE_GEMINI_API_KEY"
4️⃣ Run the Application
bash
Copy
Edit
python main.py
🎯 Usage
The assistant will listen for your command.

It will evaluate the task and display the description.

The assistant generates Python code to complete the task.

It automatically executes the generated code.

You get real-time voice feedback and execution results.

🚀 Example Commands
✅ "Open Google" → Opens Google in the browser.
✅ "Create a folder named 'test'" → Generates and runs Python code to create the folder.
✅ "Get current weather in New York" → Fetches weather data using Python requests.
✅ "Generate a random password" → Creates and displays a secure random password.

🔥 Tech Stack
Google Gemini 2.0 Flash – AI-powered task evaluation & code generation

Python 3.x – Backend programming

SpeechRecognition – For voice input

Pyttsx3 – For text-to-speech feedback

Subprocess & OS – For script execution

✅ Enhancements & To-Do
 Voice-controlled task execution

 Automatic script generation

 Task history and logs

 GUI improvements (custom themes)

 Security prompts before executing scripts

📄 License
This project is licensed under the MIT License. Feel free to use and modify it.

🤝 Contributing
Contributions are welcome!

Fork the repository

Create a new branch (git checkout -b feature-branch)

Commit your changes (git commit -m "Add new feature")

Push to the branch (git push origin feature-branch)

Open a Pull Request

📬 Contact
GitHub: Your GitHub Profile
Email: your-email@example.com

pgsql
Copy
Edit

---

### ✅ **💡 Next Steps**

1. **Create a `requirements.txt`**:
```bash
pip freeze > requirements.txt
Push to GitHub

bash
Copy
Edit
git add .
git commit -m "Initial commit"
git push origin main

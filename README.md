
# 🎙️ JarvisAI – AI-Powered Task Automation Assistant 🚀

**JarvisAI** is an advanced AI-powered voice assistant that listens to voice commands, evaluates the task, generates the appropriate Python code, and automatically executes it.  
Powered by **Google Gemini-2.0-Flash** for intelligent code generation and task handling.

---

## 🔥 **Features**

✅ Voice recognition using speech_recognition  
✅ AI-powered task evaluation and Python code generation using Google Gemini  
✅ Automatic execution of generated code  
✅ Real-time speech feedback with pyttsx3  
✅ Error handling and feedback  

---

## 📂 **Project Structure**

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

---

## ⚙️ **Setup Instructions**

### 1️⃣ Clone the repository
Clone the project from GitHub:
git clone https://github.com/your-username/JarvisAI.git
cd JarvisAI

### 2️⃣ Install Dependencies
Install the required Python packages:
pip install -r requirements.txt

### 3️⃣ Set Up Google Gemini API
1. Go to Google AI Studio  
2. Generate your API key.  
3. Add it to the config.py file:
# /config.py
GEMINI_API_KEY = "YOUR_GOOGLE_GEMINI_API_KEY"

### 4️⃣ Run the Application
Start the assistant:
python main.py

---

## 🎯 **Usage**

1. The assistant will listen for your command.  
2. It will evaluate the task and display the description.  
3. The assistant generates Python code to complete the task.  
4. It automatically executes the generated code.  
5. You get real-time voice feedback and execution results.  

---

## 🚀 **Example Commands**

✅ "Open Google" → Opens Google in the browser.  
✅ "Create a folder named 'test'" → Generates and runs Python code to create the folder.  
✅ "Get current weather in New York" → Fetches weather data using Python requests.  
✅ "Generate a random password" → Creates and displays a secure random password.  

---

## 🔥 **Tech Stack**

- Google Gemini 2.0 Flash – AI-powered task evaluation & code generation  
- Python 3.x – Backend programming  
- SpeechRecognition – For voice input  
- Pyttsx3 – For text-to-speech feedback  
- Subprocess & OS – For script execution  

---

## ✅ **Enhancements & To-Do**

- [x] Voice-controlled task execution  
- [x] Automatic script generation  
- [ ] Task history and logs  
- [ ] GUI improvements (custom themes)  
- [ ] Security prompts before executing scripts  

---

## 📄 **License**
This project is licensed under the MIT License.  
Feel free to use and modify it.

---

## 🤝 **Contributing**

Contributions are welcome!  
1. Fork the repository  
2. Create a new branch:  
git checkout -b feature-branch  
3. Commit your changes:  
git commit -m "Add new feature"  
4. Push to the branch:  
git push origin feature-branch  
5. Open a Pull Request  

---

## 📬 **Contact**

- GitHub: Your GitHub Profile  
- Email: axeeddis@gmail.com  

---




# /mnt/data/task_manager.py
import os
import subprocess
import pyttsx3
from ai_engine import evaluate_task, generate_code_for_task

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    """Text-to-speech output."""
    print(f"🔊 {text}")
    engine.say(text)
    engine.runAndWait()

def execute_task(user_input):
    """Executes the user task by generating and running the code."""
    try:
        # Step 1: Evaluate the task
        speak("Evaluating the task.")
        task_description = evaluate_task(user_input)
        print(f"✅ Task: {task_description}")
        speak(f"Task identified: {task_description}")

        # Step 2: Generate code
        speak("Generating code.")
        code = generate_code_for_task(task_description)

        # Display the sanitized code in the terminal
        print("\n🔥 Generated Code (Sanitized):\n")
        print(code)
        print("\n------------------------------------\n")

        # Save the cleaned code to the script
        script_path = "generated_task.py"
        with open(script_path, "w") as file:
            file.write(code)

        # Step 3: Execute the script and display the result
        speak("Executing the task.")
        result = subprocess.run(["python", script_path], capture_output=True, text=True)

        if result.stdout:
            print(f"✅ Output:\n{result.stdout}")
            speak("Task completed successfully.")
        else:
            print(f"⚠️ No Output or Silent Execution.")
            speak("Task completed with no visible output.")

        if result.stderr:
            print(f"❌ Error:\n{result.stderr}")
            speak("An error occurred during execution.")
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        speak(f"An error occurred: {str(e)}")

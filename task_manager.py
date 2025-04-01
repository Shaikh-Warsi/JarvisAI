import os
import subprocess
import asyncio
from predefined_tasks import *
from ai_engine import evaluate_task, generate_code_for_task, find_application_path
import re

def speak(text):
    """Speaks the given text using espeak-ng."""
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['espeak-ng', text])
        elif os.name == 'posix':  # Linux/macOS
            subprocess.run(['espeak-ng', text])
    except FileNotFoundError:
        print("espeak-ng not found. Falling back to pyttsx3")
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"❌ Speak Error: {e}")

def find_app_locally(app_name):
    """Searches for the application locally."""
    for drive in [d + ":" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(d + ":")]:
        for root, dirs, files in os.walk(drive):
            for file in files:
                if app_name.lower() in file.lower() and file.lower().endswith(".exe"):
                    return os.path.join(root, file)
    return None

def install_missing_modules(code):
    """Installs missing Python modules from the generated code."""
    modules = re.findall(r"import (\w+)", code) + re.findall(r"from (\w+)", code)
    for module in modules:
        try:
            __import__(module)  # Check if module is already installed
        except ImportError:
            try:
                subprocess.check_call(['pip', 'install', module])
                print(f"✅ Installed missing module: {module}")
            except Exception as e:
                print(f"❌ Failed to install module: {module} - {e}")

async def execute_task(user_input):
    """Executes the user task with pre-defined tasks first, then Gemini if needed."""
    try:
        parts = user_input.split()
        command = parts[0].lower()
        args = " ".join(parts[1:])

        # Pre-defined task execution
        if "open" in user_input:
            if args.startswith("http") or ".com" in args:
                response = open_website(args)
            elif "google" in args.lower():
                response = open_website("https://www.google.com")
            else:
                app_path = find_app_locally(args)
                if app_path:
                    response = open_app(app_path)
                else:
                    app_path = await find_application_path(args)
                    if "application not found" in app_path.lower():
                        response = f"Could not find application: {args}"
                    else:
                        response = open_app(app_path)
        elif "shutdown" in user_input:
            response = shutdown()
        elif "restart" in user_input:
            response = restart()
        elif "sleep" in user_input:
            response = sleep()
        elif "create" in user_input:
            response = create_file(args)
        elif "delete" in user_input:
            response = delete_file(args)
        elif "write" in user_input:
            lang, *task = args.split()
            code = await generate_code_for_task(" ".join(task), lang)
            with open(f"generated_code.{lang}", 'w') as f:
                f.write(code)
            response = f"Generated {lang} code and saved as generated_code.{lang}"
        elif "read" in user_input:
            if "mail" in args:
                response = read_emails()
            else:
                response = "Unknown read command."
        elif "send" in user_input:
            try:
                subject, body, recipient = args.split(';')
                response = send_email(subject, body, recipient)
            except ValueError:
                response = "Invalid email format. Use: send subject; body; recipient"
        else:
            # Default to Gemini for unknown commands
            task_description = await evaluate_task(user_input)
            code = await generate_code_for_task(task_description)
            install_missing_modules(code)
            script_path = "generated_task.py"
            with open(script_path, "w") as file:
                file.write(code)
            os.system(f"python {script_path}")
            response = "Executed with Gemini-generated code."

        print(f"✅ {response}")
        speak(response)
    except Exception as e:
        print(f"❌ Exception: {e}")
        speak(f"An error occurred: {str(e)}")
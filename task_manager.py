import os
import subprocess
import asyncio
from ai_engine import evaluate_task, generate_code_for_task, find_application_path, generate_content_for_task
import re
import queue
import logging
import webbrowser

# Configure logging (optional)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

task_queue = queue.Queue()
task_history = []

def speak(text):
    # Replace with your actual text-to-speech implementation
    print(text)  # For demonstration purposes
    pass

def find_app_locally(app_name):
    # Replace with your local application search logic
    # Example (Windows):
    try:
        result = subprocess.run(['where', app_name], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def open_app(app_path):
    try:
        subprocess.Popen([app_path])
        return f"Opened application: {app_path}"
    except Exception as e:
        return f"Error opening application: {e}"

def shutdown():
    try:
        subprocess.run(['shutdown', '/s', '/t', '1'], check=True)
        return "Shutting down system."
    except Exception as e:
        return f"Error shutting down: {e}"

def restart():
    try:
        subprocess.run(['shutdown', '/r', '/t', '1'], check=True)
        return "Restarting system."
    except Exception as e:
        return f"Error restarting: {e}"

def sleep():
    try:
        subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'], check=True)
        return "Putting system to sleep."
    except Exception as e:
        return f"Error putting system to sleep: {e}"

def create_file(file_path):
    try:
        with open(file_path, 'w') as f:
            f.write('')
        return f"Created file: {file_path}"
    except Exception as e:
        return f"Error creating file: {e}"

def delete_file(file_path):
    try:
        os.remove(file_path)
        return f"Deleted file: {file_path}"
    except Exception as e:
        return f"Error deleting file: {e}"

def read_emails():
    # Replace with your email reading logic (e.g., using IMAP)
    return "Email reading not implemented."

def send_email(subject, body, recipient):
    # Replace with your email sending logic (e.g., using SMTP)
    return "Email sending not implemented."

async def async_open_website(url):
    """Opens a website asynchronously."""
    try:
        await asyncio.to_thread(webbrowser.open, url)
        logging.info(f"Opened website: {url}")
        return f"Opened {url}"
    except Exception as e:
        logging.error(f"Error opening website {url}: {e}")
        return f"Error opening {url}: {e}"

async def process_task(task_description):
    # Replace with your task processing logic
    return f"Processed task: {task_description}"

async def evaluate_and_execute(user_input):
    """Evaluates the task using Gemini and executes accordingly."""
    try:
        evaluation_prompt = f"""
        Analyze the following user command and determine if the user wants to open a website or an application.
        If it's a website, extract the URL. If it's an application, extract the application name.
        Return the result in the following format:
        Type: website or application
        Value: URL or application name

        Command: {user_input}
        """
        evaluation_result = await generate_content_for_task(evaluation_prompt)
        if evaluation_result is None:
            return "Gemini model error."
        evaluation_text = evaluation_result.text
        logging.info(f"Gemini evaluation: {evaluation_text}")

        type_match = re.search(r"Type:\s*(website|application)", evaluation_text, re.IGNORECASE)
        value_match = re.search(r"Value:\s*(.+)", evaluation_text)

        if type_match and value_match:
            task_type = type_match.group(1).lower()
            value = value_match.group(1).strip()

            if task_type == "website":
                return await async_open_website(value)
            elif task_type == "application":
                app_path = find_app_locally(value)
                if app_path:
                    return open_app(app_path)
                else:
                    app_path = await find_application_path(value)
                    if "application not found" in app_path.lower():
                        return f"Could not find application: {value}"
                    else:
                        return open_app(app_path)
        else:
            return "Could not understand the command."

    except Exception as e:
        logging.error(f"Error evaluating and executing: {e}", exc_info=True)
        return f"Error: {e}"

async def execute_task(user_input):
    """Executes the user task, handling planning and queuing."""
    try:
        parts = user_input.split()
        command = parts[0].lower()
        args = " ".join(parts[1:])

        response = None  # initialize response variable

        if "open" in user_input:
            response = await evaluate_and_execute(user_input)
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
            prompt = f"""
            Write a Python script that will:
            1. Create a new folder called 'my_scripts' if it doesn't exist.
            2. Create a Python file called 'my_script.py' inside the 'my_scripts' folder.
            3. Write the following Python code into the 'my_script.py' file: {args}
            Only output the executable python code.
            Do not include any comments or explanations in the generated code.
            """
            generated_code = await generate_code_for_task(prompt)
            if generated_code:
                generated_code = re.sub(r"```(?:python)?\n?([\s\S]*?)```", r"\1", generated_code).strip()
                print(f"Cleaned generated code: {generated_code}")
                try:
                    exec(generated_code)
                    response = "Code executed"
                except Exception as e:
                    response = f"Error executing code: {e}"
            else:
                response = "Failed to generate code."
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
        elif "plan" in user_input:
            task_description = await evaluate_task(user_input)
            speak(f"Planning: {task_description}")
            task_queue.put(task_description)
            speak("Task added to queue")
        else:
            task_description = await evaluate_task(user_input)
            task_queue.put(task_description)
            speak(f"Task added to queue: {task_description}")

        if not task_queue.empty():
            while not task_queue.empty():
                current_task = task_queue.get()
                response = await process_task(current_task)
                speak(response)
                task_history.append(current_task)

        logging.info(f"Task '{user_input}' completed with response: {response}")

    except Exception as e:
        logging.error(f"Exception during task '{user_input}': {e}", exc_info=True)
        print(f"❌ Exception: {e}")
        speak(f"An error occurred: {str(e)}")

        if response is None:
            response = f"Error: {e}"
        logging.info(f"Task '{user_input}' completed with response: {response}")

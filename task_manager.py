# task_manager.py
import os
import subprocess
import asyncio
from ai_engine import evaluate_task, generate_code_for_task, find_application_path, generate_content_for_task, list_available_models
import re
import queue
import logging
import webbrowser
import system_control
import app_control
import web_automation
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

task_queue = queue.Queue()
task_history = []
conversation_history = []
stored_code = None

def speak(text):
    print(text)
    pass

def find_app_locally(app_name):
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
    return system_control.shutdown_pc()

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
    return "Email reading not implemented."

def send_email(subject, body, recipient):
    return "Email sending not implemented."

async def async_open_website(url):
    try:
        await asyncio.to_thread(webbrowser.open, url)
        logging.info(f"Opened website: {url}")
        return f"Opened {url}"
    except Exception as e:
        logging.error(f"Error opening website {url}: {e}")
        return f"Error opening {url}: {e}"

async def process_task(task_description):
    return f"Processed task: {task_description}"

async def evaluate_and_execute(user_input):
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
        evaluation_text = evaluation_result
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

def save_and_open_code(code_content, base_filename="my_script"):
    """
    Saves the given code content to a new file with a timestamped name,
    creates the 'my_scripts' folder if necessary, and opens the folder.
    """

    folder_name = 'my_scripts'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    timestamp = time.strftime("%Y%m%d%H%M%S")
    file_name = f"{base_filename}_{timestamp}.py"
    file_path = os.path.join(folder_name, file_name)

    with open(file_path, 'w') as f:
        f.write(code_content)

    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(f'explorer "{os.path.abspath(folder_name)}"')
        elif os.name == 'posix':  # macOS or Linux
            subprocess.Popen(['open', os.path.abspath(folder_name)])  # macOS
            #subprocess.Popen(['xdg-open', os.path.abspath(folder_name)]) # linux
        print(f"Code saved to {file_path} and folder opened.")
    except Exception as e:
        print(f"Code saved to {file_path}, but could not open folder: {e}")

async def execute_task(user_input):
    global stored_code
    try:
        parts = user_input.split()
        command = parts[0].lower()
        args = " ".join(parts[1:])

        response = None
        context = ""

        if conversation_history:
            context = "\n".join([f"User: {turn['user']}\nAI: {turn['ai']}" for turn in conversation_history[-3:]])
            context += "\n"

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
            {context}
            Write a Python script that will:
            {args}
            Only output the executable python code.
            Do not include any comments or explanations in the generated code.
            """
            generated_code = await generate_code_for_task(prompt)
            if generated_code:
                generated_code = re.sub(r"```(?:python)?\n?([\s\S]*?)```", r"\1", generated_code).strip()
                try:
                    save_and_open_code(generated_code)
                    response = "Code saved and folder opened."
                    stored_code = generated_code
                except Exception as e:
                    response = f"Error saving code: {e}"
            else:
                response = "Failed to generate code."

        elif "make a ui for it" in user_input:
            if stored_code:
                prompt = f"""
                {context}
                Modify the following python code to implement a user interface using PyQt5.
                {stored_code}
                Only output the executable python code.
                Do not include any comments or explanations in the generated code.
                """
                generated_code = await generate_code_for_task(prompt)
                if generated_code:
                    generated_code = re.sub(r"```(?:python)?\n?([\s\S]*?)```", r"\1", generated_code).strip()
                    try:
                        save_and_open_code(generated_code, "my_ui")
                        response = "Code saved and folder opened."
                        stored_code = generated_code
                    except Exception as e:
                        response = f"Error saving code: {e}"
                else:
                    response = "Failed to generate code."
            else:
                response = "No previous code to modify."

        elif "explain" in user_input:
            prompt = f"""
            {context}
            {user_input}
            Only explain the code, do not output the code.
            """
            task_description = await evaluate_task(prompt)
            task_queue.put(task_description)
            speak(f"Task added to queue: {task_description}")
        elif "list models" in user_input:
            models = await list_available_models()
            response = "\n".join(models) if models else "Failed to retrieve model list"
        elif "volume" in user_input:
            try:
                percentage = int(user_input.split("volume ")[1])
                response = system_control.control_volume(percentage)
            except ValueError:
                response = "Invalid volume percentage."
        elif "launch" in user_input:
            app_path = user_input.split("launch ")[1]
            response = system_control.launch_app(app_path)
        elif "notepad" in user_input:
            if len(parts) > 1:
                text = user_input.split("notepad ")[1]
                response = app_control.control_notepad(text)
            else:
                response = system_control.launch_app("notepad.exe")
        elif "search" in user_input:
            query = user_input.split("search ")[1]
            response = web_automation.search_google(query)
        else:
            prompt = f"""
            {context}
            {user_input}
            """
            task_description = await evaluate_task(prompt)
            task_queue.put(task_description)
            speak(f"Task added to queue: {task_description}")

        if not task_queue.empty():
            while not task_queue.empty():
                current_task = task_queue.get()
                response = await process_task(current_task)
                speak(response)
                task_history.append(current_task)

        logging.info(f"Task '{user_input}' completed with response: {response}")

        if response:
            conversation_history.append({"user": user_input, "ai": response})

    except Exception as e:
        logging.error(f"Exception during task '{user_input}': {e}", exc_info=True)
        print(f"❌ Exception: {e}")
        speak(f"An error occurred: {str(e)}")
        response = f"Error: {e}"

    if response is None:
        response = "Unknown Error"
    logging.info(f"Task '{user_input}' completed with response: {response}")
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

async def evaluate_task(user_input):
    """Evaluates the task from the user's input using Gemini."""
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"""
    You are an advanced AI assistant. 
    Analyze the following user command and describe the task clearly in a single sentence:
    
    Command: "{user_input}"
    Task Description:
    """
    response = await model.generate_content_async(prompt)
    return response.text.strip()

def sanitize_code(code):
    """Remove backticks and unnecessary formatting."""
    return code.replace("```python", "").replace("```", "").strip()

async def generate_code_for_task(task_description, language="python"):
    """Generates code for the given task using Gemini."""
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"""
    Write a COMPLETE {language} script to perform the following task:

    Task: {task_description}

    - Import the TaskManager class from the task_manager module.
    - Create an instance of the TaskManager class from the imported class.
    - Use the speak method of the TaskManager instance to speak the result.
    - Do NOT include any pip install commands.
    - Example: from task_manager import TaskManager; TaskManager().speak("Text to speak")
    - Do NOT include ``` or any code block formatting.
    - Only return plain {language} code without explanations or comments.
    """
    response = await model.generate_content_async(prompt)
    return sanitize_code(response.text.strip())

async def find_application_path(app_name):
    """Uses Gemini to find the application path."""
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"""
    Find the complete file path of the application "{app_name}" on the system.
    If the application is not found, return "Application not found".
    Return the path, and ONLY the path.
    """
    response = await model.generate_content_async(prompt)
    return response.text.strip()
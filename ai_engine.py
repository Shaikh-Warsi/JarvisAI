# /mnt/data/ai_engine.py
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure Gemini with API key
genai.configure(api_key=GEMINI_API_KEY)

def evaluate_task(user_input):
    """Evaluates the task from the user's input using Gemini."""
    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = f"""
    You are an advanced AI assistant. 
    Analyze the following user command and describe the task clearly in a single sentence:
    
    Command: "{user_input}"
    Task Description:
    """
    
    response = model.generate_content(prompt)
    
    # Extract the task description from the response
    task_description = response.text.strip()
    return task_description


def sanitize_code(code):
    """Remove backticks and unnecessary formatting."""
    # Strip backticks, spaces, and extra formatting
    clean_code = code.replace("```python", "").replace("```", "").strip()
    return clean_code


def generate_code_for_task(task_description):
    """Generates Python code for the given task using Gemini."""
    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = f"""
    Write a COMPLETE Python script to perform the following task:
    
    Task: {task_description}
    
    - Use appropriate Python libraries like `os`, `webbrowser`, `subprocess`, etc.
    - Ensure the code performs the task automatically on execution.
    - Do NOT include ``` or any code block formatting.
    - Only return plain Python code without explanations or comments.
    """
    
    response = model.generate_content(prompt)

    # Sanitize the generated code
    raw_code = response.text.strip()
    clean_code = sanitize_code(raw_code)
    
    return clean_code

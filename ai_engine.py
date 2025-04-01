import google.generativeai as genai
from config import GEMINI_API_KEY
import os

genai.configure(api_key=GEMINI_API_KEY)

# Adjust the model name here based on the Gemini 2.0 Flash model identifier
model_name = 'gemini-2.0-flash' #This is a placeholder, check the google docs.
#If that model name does not work, use the list models function from the last response.
try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    print(f"Error initializing model: {e}")
    model = None

async def generate_code_for_task(task_description, language="python"):
    """Generates code for a given task description."""
    if model is None:
        return "Model initialization failed."
    prompt = f"Write {language} code to {task_description}."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating code: {e}")
        return None

async def evaluate_task(task_description):
    """Evaluates the task and provides a more detailed description."""
    if model is None:
        return "Model initialization failed."
    prompt = f"Provide a detailed description of the task: {task_description}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error evaluating task: {e}")
        return None

async def find_application_path(app_name):
    """Tries to find the application path using Gemini."""
    if model is None:
        return "Model initialization failed."
    prompt = f"Find the full path to the application '{app_name}' on a Windows system. If not found, return 'application not found'."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error finding application path: {e}")
        return None

async def generate_content_for_task(prompt):
    """Generates content based on a given prompt."""
    if model is None:
        return "Model initialization failed."
    try:
        response = model.generate_content(prompt)
        return response
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

def list_available_models():
    """Lists available models."""
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f'{m.name}: {m.description}')

#list_available_models() #use this to print the available models.

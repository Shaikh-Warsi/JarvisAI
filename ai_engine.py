# ai_engine.py
import google.generativeai as genai
from config import GOOGLE_API_KEY  # Assuming you have GOOGLE_API_KEY in config.py
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

genai.configure(api_key=GOOGLE_API_KEY)

async def generate_content_for_task(prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Error generating content: {e}", exc_info=True)
        return None

async def generate_code_for_task(task_description, language="python"):
    prompt = f"Write {language} code to {task_description}."
    return await generate_content_for_task(prompt)

async def evaluate_task(task_description):
    prompt = f"Provide a detailed description of the task: {task_description}"
    return await generate_content_for_task(prompt)

async def find_application_path(app_name):
    prompt = f"Find the full path to the application '{app_name}' on a Windows system. If not found, return 'application not found'."
    return await generate_content_for_task(prompt)

async def list_available_models():
    try:
        models = [model.name for model in genai.list_models()]
        return models
    except Exception as e:
        logging.error(f"Error listing models: {e}", exc_info=True)
        return None
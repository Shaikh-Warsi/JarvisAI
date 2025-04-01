import os
import webbrowser
import subprocess
import smtplib
from email.mime.text import MIMEText
import imaplib
import email
from config import EMAIL_USER, EMAIL_PASSWORD

def open_website(url):
    webbrowser.open(url)
    return f"Opened {url}"

def open_app(app_path):
    try:
        subprocess.Popen(app_path)
        return f"Opened {app_path}"
    except FileNotFoundError:
        return f"Could not find application: {app_path}"
def open_website(url):
    webbrowser.open(url)
    return f"Opened {url}"

def open_app(app_name):
    try:
        if app_name.lower() == "chrome":
            subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe") #or the x86 path
            return f"Opened Chrome"
        else:
            subprocess.Popen(app_name)
            return f"Opened {app_name}"
    except FileNotFoundError:
        return f"Could not find application: {app_name}"

def shutdown():
    os.system("shutdown /s /t 1")
    return "Shutting down the system."

def restart():
    os.system("shutdown /r /t 1")
    return "Restarting the system."

def sleep():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    return "Putting the system to sleep."

def create_file(filename):
    open(filename, 'w').close()
    return f"Created file: {filename}"

def delete_file(filename):
    try:
        os.remove(filename)
        return f"Deleted file: {filename}"
    except FileNotFoundError:
        return f"File not found: {filename}"

def write_code(language, task):
    # Example using Gemini for code generation
    from ai_engine import generate_code_for_task
    description = f"Write {language} code to {task}"
    code = generate_code_for_task(description)
    with open(f"generated_code.{language}", 'w') as f:
        f.write(code)
    return f"Generated {language} code and saved as generated_code.{language}"

def read_emails():
    try:
        mail = imaplib.IMAP4_SSL('[imap.gmail.com](https://www.google.com/search?q=imap.gmail.com)')
        mail.login(EMAIL_USER, EMAIL_PASSWORD)
        mail.select('inbox')

        _, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = data[0].split()

        messages = []
        for num in id_list[-5:]:  # Get last 5 emails
            _, data = mail.fetch(num, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg['subject']
                    from_ = msg['from']
                    messages.append(f"From: {from_}, Subject: {subject}")
        mail.close()
        mail.logout()
        return "\n".join(messages) if messages else "No emails found."

    except Exception as e:
        return f"Error reading emails: {e}"

def send_email(subject, body, recipient):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = recipient

        with smtplib.SMTP_SSL('[smtp.gmail.com](https://www.google.com/search?q=smtp.gmail.com)', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return "Email sent successfully."
    except Exception as e:
        return f"Error sending email: {e}"
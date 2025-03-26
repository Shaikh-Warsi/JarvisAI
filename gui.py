import sys
import threading
import queue
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
import speech_engine
import task_manager

class SciFiAssistant(QMainWindow):
    def __init__(self):
        super().__init__()

        # ✅ Window Setup
        self.setWindowTitle("Sci-Fi AI Assistant")
        self.setGeometry(400, 200, 600, 600)
        self.setStyleSheet("background-color: black;")

        # ✅ Centered AI GIF
        self.ai_visual = QLabel(self)
        self.ai_visual.setGeometry(150, 150, 300, 300)
        self.ai_visual.setAlignment(Qt.AlignCenter)
        self.ai_visual.setStyleSheet("background-color: transparent;")

        self.movie = QMovie("ai_wave.gif")  # ✅ Ensure the GIF exists
        self.movie.setScaledSize(self.ai_visual.size())
        self.ai_visual.setMovie(self.movie)
        self.movie.start()

        # ✅ Status Display
        self.status_label = QLabel("Listening Mode: ON", self)
        self.status_label.setGeometry(100, 500, 400, 40)
        self.status_label.setStyleSheet("color: #00FF00; font-size: 16px; font-family: Courier;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # ✅ Text Input for Manual Commands
        self.command_input = QLineEdit(self)
        self.command_input.setGeometry(100, 450, 400, 40)
        self.command_input.setPlaceholderText("Type your command here...")
        self.command_input.setStyleSheet("color: #FFFFFF; font-size: 14px; background-color: #333333; padding: 5px;")
        self.command_input.returnPressed.connect(self.process_text_input)
        self.command_input.setVisible(False)  # Initially hidden

        # ✅ Toggle Button for Mode Switching
        self.toggle_button = QPushButton("Switch to Typing Mode", self)
        self.toggle_button.setGeometry(200, 550, 200, 40)
        self.toggle_button.setStyleSheet("background-color: #444444; color: white; font-size: 14px;")
        self.toggle_button.clicked.connect(self.toggle_mode)

        # ✅ Start AI Listening Thread
        self.listening = True  # Default mode: Listening
        self.thread = threading.Thread(target=self.listen_and_process, daemon=True)
        self.thread.start()

    def listen_and_process(self):
        """Continuously listens and executes tasks when in listening mode."""
        while True:
            if self.listening:
                self.status_label.setText("Listening... Speak now.")
                user_input = speech_engine.listen()
                if user_input.strip():
                    self.status_label.setText(f"Processing: {user_input}")
                    task_manager.execute_task(user_input)
    
    def process_text_input(self):
        """Handles text input when Typing Mode is enabled."""
        if not self.listening:  # Only process if in Typing Mode
            user_input = self.command_input.text().strip()
            if user_input:
                self.status_label.setText(f"Processing: {user_input}")
                task_manager.execute_task(user_input)
                self.command_input.clear()
    
    def toggle_mode(self):
        """Switches between Listening Mode and Typing Mode."""
        self.listening = not self.listening
        if self.listening:
            self.status_label.setText("Listening Mode: ON")
            self.command_input.setVisible(False)
            self.toggle_button.setText("Switch to Typing Mode")
        else:
            self.status_label.setText("Typing Mode: ON")
            self.command_input.setVisible(True)
            self.toggle_button.setText("Switch to Listening Mode")


def run_gui():
    """Launch the AI Assistant GUI."""
    app = QApplication(sys.argv)
    window = SciFiAssistant()
    window.show()
    sys.exit(app.exec_())
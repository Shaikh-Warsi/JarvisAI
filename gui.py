import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QMovie, QFont, QPainter, QColor, QBrush, QRegion
from PyQt5.QtCore import Qt, QSize, QPoint
import speech_engine
import task_manager
import asyncio

class SciFiAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.listening = True
        self.drag_pos = None
        self.init_ui()
        self.thread = threading.Thread(target=self.listen_and_process, daemon=True)
        self.thread.start()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(300, 100, 850, 600)

        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
            background: rgba(0, 0, 0, 240); 
            border-radius: 30px; 
            border: 2px solid #00FFFF;
        """)

        self.close_button = QPushButton("✖", self)
        self.close_button.setGeometry(780, 10, 50, 50)
        self.close_button.setStyleSheet("""
            color: #FF5555; 
            font-size: 24px; 
            background: transparent;
        """)
        self.close_button.clicked.connect(self.close)

        self.minimize_button = QPushButton("➖", self)
        self.minimize_button.setGeometry(720, 10, 50, 50)
        self.minimize_button.setStyleSheet("""
            color: #55FF55; 
            font-size: 24px; 
            background: transparent;
        """)
        self.minimize_button.clicked.connect(self.showMinimized)

        self.ai_visual = QLabel(self)
        self.ai_visual.setGeometry(150, 100, 550, 350)
        self.ai_visual.setAlignment(Qt.AlignCenter)
        self.ai_visual.setStyleSheet("background: transparent;")

        self.movie = QMovie("ai_wave.gif")
        self.movie.setScaledSize(QSize(550, 350))
        self.ai_visual.setMovie(self.movie)
        self.movie.start()

        self.status_label = QLabel("Listening Mode: ON", self)
        self.status_label.setGeometry(100, 470, 650, 40)
        self.status_label.setStyleSheet("""
            color: #00FF00; 
            font-size: 20px; 
            font-family: 'Orbitron'; 
            background: transparent;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)

        self.command_input = QLineEdit(self)
        self.command_input.setGeometry(100, 520, 650, 40)
        self.command_input.setPlaceholderText("Type your command here...")
        self.command_input.setStyleSheet("""
            color: #FFFFFF; 
            font-size: 16px; 
            background: rgba(255, 255, 255, 0.1); 
            border: 2px solid #00FFFF; 
            border-radius: 12px; 
            padding: 10px;
        """)
        self.command_input.returnPressed.connect(self.process_text_input)
        self.command_input.setVisible(False)

        self.toggle_button = QPushButton("Switch to Typing Mode", self)
        self.toggle_button.setGeometry(330, 570, 200, 45)
        self.toggle_button.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #00FFFF, stop:1 #0055FF);
            color: white; 
            font-size: 16px; 
            border-radius: 15px; 
            padding: 12px;
        """)
        self.toggle_button.clicked.connect(self.toggle_mode)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

    def listen_and_process(self):
        asyncio.run(self.async_listen_and_process())

    async def async_listen_and_process(self):
        while True:
            if self.listening:
                self.status_label.setText("Listening... Speak now.")
                user_input = await speech_engine.listen()
                if user_input and user_input.strip():
                    self.status_label.setText(f"Processing: {user_input}")
                    await task_manager.execute_task(user_input)

    def process_text_input(self):
        if not self.listening:
            user_input = self.command_input.text().strip()
            if user_input:
                self.status_label.setText(f"Processing: {user_input}")
                asyncio.run(task_manager.execute_task(user_input))
                self.command_input.clear()

    def toggle_mode(self):
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
    app = QApplication(sys.argv)
    window = SciFiAssistant()
    window.show()
    sys.exit(app.exec_())
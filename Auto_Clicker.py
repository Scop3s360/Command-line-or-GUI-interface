import sys
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                            QWidget, QPushButton, QHBoxLayout, QFrame, QDesktopWidget)
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QFont, QIcon
from pynput.mouse import Button, Controller, Listener
import keyboard
import time

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        
        # Title with icon
        self.title = QLabel("Auto Clicker")
        self.title.setStyleSheet("""
            color: white;
            padding: 4px;
            font-weight: bold;
            font-size: 12px;
        """)

        # Minimize button
        btn_size = 35
        self.btn_minimize = QPushButton('−')
        self.btn_minimize.setFixedSize(btn_size, 20)
        self.btn_minimize.clicked.connect(self.parent.showMinimized)
        self.btn_minimize.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0);
                color: white;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 30);
            }
        """)

        # Close button
        self.btn_close = QPushButton('×')
        self.btn_close.setFixedSize(btn_size, 20)
        self.btn_close.clicked.connect(self.parent.close)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0);
                color: white;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: red;
            }
        """)

        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.layout.addWidget(self.btn_minimize)
        self.layout.addWidget(self.btn_close)
        
        self.setLayout(self.layout)
        
        self.setStyleSheet("""
            background-color: rgba(40, 40, 40, 255);
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        """)

class AutoClickerOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Initialize variables
        self.clicking = False
        self.click_delay = 1.0  # Default delay in seconds
        self.mouse = Controller()
        self.dragging = False
        self.offset = QPoint()
        self.click_count = 0  # Counter for clicks

        # Create the UI
        self.initUI()
        
        # Center the window
        self.center()
        
        # Start the clicking thread
        self.click_thread = threading.Thread(target=self.auto_click, daemon=True)
        self.click_thread.start()

        # Setup keyboard listeners
        keyboard.on_press_key('f6', lambda _: self.toggle_clicking())
        keyboard.on_press_key('f7', lambda _: self.increase_speed())
        keyboard.on_press_key('f8', lambda _: self.decrease_speed())

        # Setup mouse listener for right click
        self.mouse_listener = Listener(on_click=self.on_click)
        self.mouse_listener.start()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def initUI(self):
        self.setFixedSize(250, 220)
        
        # Create main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        # Add title bar
        self.title_bar = TitleBar(self)
        self.main_layout.addWidget(self.title_bar)

        # Create content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(15,15,15,15)
        self.content_layout.setSpacing(10)

        # Status label
        self.status_label = QLabel('Status: Stopped')
        self.status_label.setFont(QFont('Arial', 10))
        self.status_label.setStyleSheet('color: white;')
        self.content_layout.addWidget(self.status_label)

        # Speed label
        self.speed_label = QLabel(f'Delay: {self.click_delay:.2f}s')
        self.speed_label.setFont(QFont('Arial', 10))
        self.speed_label.setStyleSheet('color: white;')
        self.content_layout.addWidget(self.speed_label)

        # Click counter label
        self.counter_label = QLabel('Clicks: 0')
        self.counter_label.setFont(QFont('Arial', 10))
        self.counter_label.setStyleSheet('color: white;')
        self.content_layout.addWidget(self.counter_label)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: rgba(255,255,255,50);")
        self.content_layout.addWidget(line)

        # Controls label
        controls_text = (
            'Controls:\n'
            'F6: Start/Stop\n'
            'F7: Speed Up\n'
            'F8: Slow Down\n'
            'Right Click: Emergency Stop'
        )
        controls_label = QLabel(controls_text)
        controls_label.setFont(QFont('Arial', 9))
        controls_label.setStyleSheet('color: white;')
        self.content_layout.addWidget(controls_label)

        # Add spacing
        self.content_layout.addSpacing(5)

        # Create horizontal layout for reset button
        reset_layout = QHBoxLayout()
        
        # Reset button
        self.reset_button = QPushButton('Reset Counter & Timer')
        self.reset_button.setFixedHeight(25)
        self.reset_button.clicked.connect(self.reset_all)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(60, 60, 60, 180);
                color: white;
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 180);
                border: 1px solid rgba(255, 255, 255, 80);
            }
            QPushButton:pressed {
                background-color: rgba(40, 40, 40, 180);
            }
        """)
        reset_layout.addWidget(self.reset_button)
        
        # Add reset layout to main content layout
        self.content_layout.addLayout(reset_layout)

        # Add content widget to main layout
        self.main_layout.addWidget(self.content_widget)

        # Set background color with transparency
        self.content_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(50, 50, 50, 180);
                border-bottom-left-radius: 5px;
                border-bottom-right-radius: 5px;
            }
        """)

    def auto_click(self):
        while True:
            if self.clicking:
                self.mouse.click(Button.left)
                self.click_count += 1
                self.counter_label.setText(f'Clicks: {self.click_count}')
            time.sleep(self.click_delay)

    def toggle_clicking(self):
        self.clicking = not self.clicking
        status_text = "Running" if self.clicking else "Stopped"
        status_color = "lime" if self.clicking else "white"
        self.status_label.setText(f'Status: {status_text}')
        self.status_label.setStyleSheet(f'color: {status_color};')

    def increase_speed(self):
        self.click_delay = max(0.01, self.click_delay - 0.1)
        self.speed_label.setText(f'Delay: {self.click_delay:.2f}s')

    def decrease_speed(self):
        self.click_delay += 0.1
        self.speed_label.setText(f'Delay: {self.click_delay:.2f}s')

    def reset_all(self):
        # Reset click counter
        self.click_count = 0
        self.counter_label.setText('Clicks: 0')
        
        # Reset timer to default
        self.click_delay = 1.0
        self.speed_label.setText(f'Delay: {self.click_delay:.2f}s')
        
        # Stop clicking if it's running
        self.clicking = False
        self.status_label.setText('Status: Stopped')
        self.status_label.setStyleSheet('color: white;')

        # Add visual feedback for reset
        self.reset_button.setText('Reset Complete!')
        QTimer.singleShot(1000, lambda: self.reset_button.setText('Reset Counter & Timer'))

    def on_click(self, x, y, button, pressed):
        if button == Button.right and pressed:
            self.clicking = False
            self.status_label.setText('Status: Stopped')
            self.status_label.setStyleSheet('color: white;')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def closeEvent(self, event):
        self.mouse_listener.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    auto_clicker = AutoClickerOverlay()
    auto_clicker.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Reference to the parent window
        self.setStyleSheet("""
            QWidget {
                background-color: #2e3440;
                color: white;
            }
        """)
        self.setFixedHeight(30)
        self._startPos = None  # For dragging the window

        # Layout for the title bar
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        # Title text
        self.title_label = QLabel("Wecap", alignment=Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 10))
        self.layout.addWidget(self.title_label)

        # Minimize button
        self.minimize_button = QPushButton("-")
        self.minimize_button.setFixedSize(25, 25)
        self.minimize_button.clicked.connect(self.minimize_window)
        self.layout.addWidget(self.minimize_button)

        # Close button
        self.close_button = QPushButton("x")
        self.close_button.setFixedSize(25, 25)
        self.close_button.clicked.connect(self.close_window)
        self.layout.addWidget(self.close_button)

    def minimize_window(self):
        if self.parent:
            self.parent.showMinimized()

    def close_window(self):
        if self.parent:
            self.parent.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._startPos = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._startPos is not None:
            self.parent.move(event.globalPos() - self._startPos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._startPos = None
            event.accept()


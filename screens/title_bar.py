from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Reference to the parent window
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
            }
            QPushButton {
                background-color: #2e3440;
                color: white;
                border: none;
                padding: 0px;
            }
        """)
        self.setFixedHeight(40)
        self._startPos = None  # For dragging the window

        # Layout for the title bar
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 10, 5)
        self.layout.setSpacing(5)

        # Placeholder to balance the layout on the left
        left_placeholder = QWidget(self)
        left_placeholder.setFixedWidth(60)  # Width of minimize and close buttons
        self.layout.addWidget(left_placeholder)

        # Title text
        self.title_label = QLabel("Wecap", alignment=Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 10))
        self.layout.addWidget(self.title_label)

        # Minimize button
        self.minimize_button = QPushButton("-")
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.clicked.connect(self.minimize_window)
        self.layout.addWidget(self.minimize_button)

        # Close button
        self.close_button = QPushButton("x")
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close_window)
        self.layout.addWidget(self.close_button)

    def minimize_window(self):
        if self.parent:
            self.parent.hide()

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


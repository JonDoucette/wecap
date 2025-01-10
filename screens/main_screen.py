from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, QTextEdit, QPushButton, QLabel
from PyQt5.QtCore import QDate, Qt

class MainScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        """Initializes the main screen layout."""
        self.top_bar = QHBoxLayout()
        self.main_layout = QVBoxLayout()

        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.accomplishment_input = QTextEdit()
        self.add_button = QPushButton("Add Accomplishment")
        self.add_button.clicked.connect(self.add_accomplishment)

        self.past_submissions_button = QPushButton("Past Submissions")

        self.top_bar.addWidget(QLabel("Date:"))
        self.top_bar.addWidget(self.date_input)

        self.main_layout.addWidget(QLabel("Accomplishment:"))
        self.main_layout.addWidget(self.accomplishment_input)
        self.main_layout.addWidget(self.add_button)
        self.main_layout.addWidget(self.past_submissions_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.top_bar)
        main_layout.addLayout(self.main_layout)

        self.setLayout(main_layout)

    def add_accomplishment(self):
        """Adds a new accomplishment to the database."""
        selected_date = self.date_input.date()
        date = selected_date.toString("yyyy-MM-dd")
        accomplishment = self.accomplishment_input.toPlainText().strip()
        if accomplishment:
            self.db_manager.add_accomplishment(date, accomplishment)
            self.accomplishment_input.clear()


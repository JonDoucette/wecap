import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QDateEdit, QTableWidget, QTableWidgetItem, QStackedWidget, QHBoxLayout
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont
from wecap_linx_stylesheet import STYLESHEET

class DatabaseManager:
    """
    Manages database operations for storing and retrieving accomplishments.
    """
    def __init__(self, db_name="wecap.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        """Creates the accomplishments table if it does not exist."""
        query = """
        CREATE TABLE IF NOT EXISTS accomplishments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            accomplishment TEXT NOT NULL
        )
        """
        self.connection.execute(query)
        self.connection.commit()

    def add_accomplishment(self, date, accomplishment):
        """Inserts a new accomplishment into the database."""
        query = "INSERT INTO accomplishments (date, accomplishment) VALUES (?, ?)"
        self.connection.execute(query, (date, accomplishment))
        self.connection.commit()

    def get_accomplishments(self, start_date=None, end_date=None):
        """Retrieves accomplishments filtered by date range, if specified."""
        if start_date and end_date:
            query = "SELECT date, accomplishment FROM accomplishments WHERE date BETWEEN ? AND ? ORDER BY date DESC"
            return self.connection.execute(query, (start_date, end_date)).fetchall()
        else:
            query = "SELECT date, accomplishment FROM accomplishments ORDER BY date DESC"
            return self.connection.execute(query).fetchall()


class GUIManager(QMainWindow):
    """
    Manages the GUI interface for inputting and viewing accomplishments.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wecap - Linux")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        """Initializes the user interface components."""
        self.stacked_widget = QStackedWidget()

        # Main Screen
        self.main_screen = QWidget()
        self.main_layout = QVBoxLayout()

        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.accomplishment_input = QTextEdit()
        self.add_button = QPushButton("Add Accomplishment")
        self.add_button.clicked.connect(self.add_accomplishment)

        self.past_submissions_button = QPushButton("Past Submissions")
        self.past_submissions_button.clicked.connect(self.show_past_submissions)

        self.close_main_button = QPushButton("X")
        self.close_main_button.clicked.connect(self.close)
        self.close_main_button.setStyleSheet('''
        background-color: red;
        ''')

        self.main_layout.addWidget(self.close_main_button, alignment=Qt.AlignTop | Qt.AlignRight)
        self.main_layout.addWidget(QLabel("Date:"))
        self.main_layout.addWidget(self.date_input)
        self.main_layout.addWidget(QLabel("Accomplishment:"))
        self.main_layout.addWidget(self.accomplishment_input)
        self.main_layout.addWidget(self.add_button)
        self.main_layout.addWidget(self.past_submissions_button)
        #self.main_layout.addWidget(self.close_main_button, alignment=Qt.AlignTop | Qt.AlignRight)

        self.main_screen.setLayout(self.main_layout)

        # Past Submissions Screen
        self.past_submissions_screen = QWidget()
        self.past_layout = QVBoxLayout()


        self.filter_layout = QHBoxLayout()

        self.start_date_input = QDateEdit(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        self.end_date_input = QDateEdit(QDate.currentDate())
        self.end_date_input.setCalendarPopup(True)

        self.filter_button = QPushButton("Filter")
        self.filter_button.clicked.connect(self.filter_accomplishments)

        self.filter_layout.addWidget(QLabel("Start Date:"))
        self.filter_layout.addWidget(self.start_date_input)
        self.filter_layout.addWidget(QLabel("End Date:"))
        self.filter_layout.addWidget(self.end_date_input)
        self.filter_layout.addWidget(self.filter_button)

        self.past_table = QTableWidget()
        self.past_table.setColumnCount(2)
        self.past_table.setHorizontalHeaderLabels(["Date", "Accomplishment"])

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.show_main_screen)

        self.close_past_button = QPushButton("X")
        self.close_past_button.clicked.connect(self.close)

        self.past_layout.addLayout(self.filter_layout)
        self.past_layout.addWidget(QLabel("Past Accomplishments:"))
        self.past_layout.addWidget(self.past_table)
        self.past_layout.addWidget(self.back_button)
        self.past_layout.addWidget(self.close_past_button, alignment=Qt.AlignTop | Qt.AlignRight)

        self.past_submissions_screen.setLayout(self.past_layout)

        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.past_submissions_screen)

        self.setCentralWidget(self.stacked_widget)

        self.refresh_table()

    def apply_styles(self):
        """Applies inline styling."""
        self.setStyleSheet(STYLESHEET)

    def add_accomplishment(self):
        """Adds a new accomplishment to the database."""
        selected_date = self.date_input.date()
        date = selected_date.toString("yyyy-MM-dd")
        accomplishment = self.accomplishment_input.toPlainText().strip()
        if accomplishment:
            db_manager.add_accomplishment(date, accomplishment)
            self.accomplishment_input.clear()

    def show_past_submissions(self):
        """Switches to the Past Submissions screen and refreshes the table."""
        self.refresh_table()
        self.stacked_widget.setCurrentWidget(self.past_submissions_screen)

    def show_main_screen(self):
        """Switches back to the Main screen."""
        self.stacked_widget.setCurrentWidget(self.main_screen)

    def refresh_table(self):
        """Refreshes the table to display the latest accomplishments."""
        data = db_manager.get_accomplishments()
        self.past_table.setRowCount(len(data))
        for row_idx, (date, accomplishment) in enumerate(data):
            self.past_table.setItem(row_idx, 0, QTableWidgetItem(date))
            self.past_table.setItem(row_idx, 1, QTableWidgetItem(accomplishment))

        # Adjust header and fill empty space
        self.past_table.horizontalHeader().setStretchLastSection(True)
        self.past_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

    def filter_accomplishments(self):
        """Filters accomplishments based on selected date range."""
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        data = db_manager.get_accomplishments(start_date, end_date)
        self.past_table.setRowCount(len(data))
        for row_idx, (date, accomplishment) in enumerate(data):
            self.past_table.setItem(row_idx, 0, QTableWidgetItem(date))
            self.past_table.setItem(row_idx, 1, QTableWidgetItem(accomplishment))

def main():
    """Main function to initialize the application."""
    global db_manager
    db_manager = DatabaseManager()
    app = QApplication(sys.argv)
    gui = GUIManager()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main();

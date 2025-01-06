import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QDateTimeEdit, QTableWidget, QTableWidgetItem, QHBoxLayout, QComboBox
)
from PyQt5.QtCore import QDateTime, QTimer
from PyQt5.QtGui import QIcon
import win10toast
import threading
import datetime

class DatabaseManager:
    def __init__(self, db_name="wecap.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS accomplishments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT NOT NULL,
            accomplishment TEXT NOT NULL
        )
        """
        self.connection.execute(query)
        self.connection.commit()

    def add_accomplishment(self, date_time, accomplishment):
        query = "INSERT INTO accomplishments (date_time, accomplishment) VALUES (?, ?)"
        self.connection.execute(query, (date_time, accomplishment))
        self.connection.commit()

    def get_accomplishments(self):
        query = "SELECT date_time, accomplishment FROM accomplishments ORDER BY date_time DESC"
        return self.connection.execute(query).fetchall()

    def is_weekly_recap_done(self):
        start_of_week = datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday())
        query = "SELECT COUNT(*) FROM accomplishments WHERE date_time >= ?"
        count = self.connection.execute(query, (start_of_week.isoformat(),)).fetchone()[0]
        return count > 0


class NotificationManager:
    def __init__(self):
        self.notifier = win10toast.ToastNotifier()

    def send_notification(self, title, message):
        self.notifier.show_toast(title, message, duration=10, threaded=True)

    def schedule_notification(self, day, time):
        def notify_task():
            while True:
                now = datetime.datetime.now()
                if now.strftime('%A') == day and now.strftime('%H:%M') == time:
                    if not db_manager.is_weekly_recap_done():
                        self.send_notification("Wecap Reminder", "Don't forget to fill out your weekly recap!")
                    threading.Event().wait(60)
        threading.Thread(target=notify_task, daemon=True).start()


class GUIManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wecap")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Input Section
        self.date_time_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.accomplishment_input = QTextEdit()
        self.add_button = QPushButton("Add Accomplishment")
        self.add_button.clicked.connect(self.add_accomplishment)

        self.layout.addWidget(QLabel("Date and Time:"))
        self.layout.addWidget(self.date_time_input)
        self.layout.addWidget(QLabel("Accomplishment:"))
        self.layout.addWidget(self.accomplishment_input)
        self.layout.addWidget(self.add_button)

        # Display Section
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Date and Time", "Accomplishment"])

        self.layout.addWidget(QLabel("Accomplishments:"))
        self.layout.addWidget(self.table)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        self.refresh_table()

    def add_accomplishment(self):
        date_time = self.date_time_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        accomplishment = self.accomplishment_input.toPlainText().strip()
        if accomplishment:
            db_manager.add_accomplishment(date_time, accomplishment)
            self.refresh_table()
            self.accomplishment_input.clear()

    def refresh_table(self):
        data = db_manager.get_accomplishments()
        self.table.setRowCount(len(data))
        for row_idx, (date_time, accomplishment) in enumerate(data):
            self.table.setItem(row_idx, 0, QTableWidgetItem(date_time))
            self.table.setItem(row_idx, 1, QTableWidgetItem(accomplishment))


if __name__ == "__main__":
    db_manager = DatabaseManager()
    notification_manager = NotificationManager()

    # Schedule notification for Friday at 17:00
    notification_manager.schedule_notification("Friday", "17:00")

    app = QApplication(sys.argv)
    gui_manager = GUIManager()
    gui_manager.show()
    sys.exit(app.exec_())


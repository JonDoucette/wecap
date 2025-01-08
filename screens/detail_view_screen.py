from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, QTextEdit, QPushButton, QLabel
from PyQt5.QtCore import QDate, Qt

class DetailScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        """Initializes the UI components"""
        self.top_bar = QHBoxLayout()
        self.layout = QVBoxLayout()

        #Add labels to display the details
        self.detail_label = QLabel("Details:")
        self.layout.addWidget(self.detail_label)

        # Back button to return to the table view
        self.back_button = QPushButton("Back")
        self.layout.addWidget(self.back_button)

        # Delete button to delete the current item
        self.delete_button = QPushButton("Delete Item")
        self.layout.addWidget(self.delete_button)

        self.setLayout(self.layout)

    def set_current_row(self, current_row):
        self.current_row = current_row

    def delete_item(self):
        self.db_manager.delete_accomplishment(self.past_submissions_screen.past_table.item(self.current_row, 0).data(Qt.UserRole))
        self.show_past_submissions()


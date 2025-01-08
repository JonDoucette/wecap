import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QDateEdit, QTableWidget, QTableWidgetItem, QStackedWidget, QHBoxLayout
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont
from wecap_linx_stylesheet import STYLESHEET

from screens.main_screen import MainScreen
from screens.past_submissions_screen import PastSubmissionsScreen
from screens.detail_view_screen import DetailScreen
from database_manager import DatabaseManager

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

        self.main_screen = MainScreen(db_manager)
        self.past_submissions_screen = PastSubmissionsScreen(db_manager)
        self.detail_screen = DetailScreen(db_manager)


        self.init_buttons()


        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.past_submissions_screen)
        self.stacked_widget.addWidget(self.detail_screen)

        self.setCentralWidget(self.stacked_widget)

        self.refresh_table()

    def init_buttons(self):
        #Buttons
        self.main_screen.close_main_button.clicked.connect(self.close)
        self.main_screen.past_submissions_button.clicked.connect(self.show_past_submissions)
        self.past_submissions_screen.past_table.itemDoubleClicked.connect(self.open_detail_window)
        self.past_submissions_screen.back_button.clicked.connect(self.show_main_screen)
        self.detail_screen.back_button.clicked.connect(self.return_to_table_view)
        self.detail_screen.delete_button.clicked.connect(self.delete_item)

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

    def show_detail_screen(self):
        # Switch to the detail view
        self.stacked_widget.setCurrentWidget(self.detail_screen)

    def setup_detail_view(self):
        layout = QVBoxLayout()

        #Add labels to display the details
        self.detail_label = QLabel("Details:")
        layout.addWidget(self.detail_label)

        # Back button to return to the table view
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.return_to_table_view)
        layout.addWidget(back_button)

        # Delete button to delete the current item
        self.delete_button = QPushButton("Delete Item")
        self.delete_button.clicked.connect(self.delete_item)
        layout.addWidget(self.delete_button)

        self.detail_view.setLayout(layout)

    def delete_item(self):
        db_manager.delete_accomplishment(self.past_submissions_screen.past_table.item(self.current_row, 0).data(Qt.UserRole))
        self.show_past_submissions()

    def open_detail_window(self, item):
        # Get data of the clicked row
        self.current_row = item.row()
        date = self.past_submissions_screen.past_table.item(self.current_row, 0).text()
        accomplishment = self.past_submissions_screen.past_table.item(self.current_row, 1).text()
        self.current_item_data = f"Date: {date}, Accomplishment: {accomplishment}"

        # Update the detail view
        self.detail_screen.detail_label.setText(f"Details:\n{self.current_item_data}")
        self.show_detail_screen()


    def return_to_table_view(self):
        self.stacked_widget.setCurrentWidget(self.past_submissions_screen)


    def refresh_table(self):
        """Refreshes the table to display the latest accomplishments."""
        data = db_manager.get_accomplishments()
        self.past_submissions_screen.past_table.setRowCount(len(data))
        for row_idx, (id_, date, accomplishment) in enumerate(data):
            self.past_submissions_screen.past_table.setItem(row_idx, 0, QTableWidgetItem(date))
            self.past_submissions_screen.past_table.setItem(row_idx, 1, QTableWidgetItem(accomplishment))

            #Store the Id as hidden data in the first column's item
            self.past_submissions_screen.past_table.item(row_idx, 0).setData(Qt.UserRole, id_)


        # Adjust header and fill empty space
        self.past_submissions_screen.past_table.horizontalHeader().setStretchLastSection(True)
        self.past_submissions_screen.past_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

    def filter_accomplishments(self):
        """Filters accomplishments based on selected date range."""
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        data = db_manager.get_accomplishments(start_date, end_date)
        self.past_submissions_screen.past_table.setRowCount(len(data))
        for row_idx, (date, accomplishment) in enumerate(data):
            self.past_submissions_screen.past_table.setItem(row_idx, 0, QTableWidgetItem(date))
            self.past_submissions_screen.past_table.setItem(row_idx, 1, QTableWidgetItem(accomplishment))

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

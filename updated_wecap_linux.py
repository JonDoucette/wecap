import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QTableWidgetItem, QStackedWidget, QVBoxLayout
)
from PyQt5.QtCore import Qt
from wecap_linx_stylesheet import STYLESHEET

from screens.main_screen import MainScreen
from screens.past_submissions_screen import PastSubmissionsScreen
from screens.detail_view_screen import DetailScreen
from screens.title_bar import CustomTitleBar
from database_manager import DatabaseManager

class GUIManager(QMainWindow):
    """
    Manages the GUI interface for inputting and viewing accomplishments.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wecap - Linux")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        """Initializes the user interface components."""
        # Central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Add custom title bar
        self.title_bar = CustomTitleBar(self)
        self.main_layout.addWidget(self.title_bar)

        # Add stacked widget for the screens
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Add screens to the stacked widget
        self.main_screen = MainScreen(db_manager)
        self.past_submissions_screen = PastSubmissionsScreen(db_manager)
        self.detail_screen = DetailScreen(db_manager)

        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.past_submissions_screen)
        self.stacked_widget.addWidget(self.detail_screen)

        self.init_buttons()

        self.refresh_table()

    def init_buttons(self):
        #Buttons
        self.main_screen.past_submissions_button.clicked.connect(self.show_past_submissions)
        self.past_submissions_screen.past_table.itemDoubleClicked.connect(self.open_detail_window)
        self.past_submissions_screen.back_button.clicked.connect(self.show_main_screen)
        self.detail_screen.back_button.clicked.connect(self.show_past_submissions)
        self.detail_screen.delete_button.clicked.connect(self.show_past_submissions)

    def apply_styles(self):
        """Applies inline styling."""
        self.setStyleSheet(STYLESHEET)

    def show_past_submissions(self):
        self.refresh_table()
        self.stacked_widget.setCurrentWidget(self.past_submissions_screen)

    def show_main_screen(self):
        self.stacked_widget.setCurrentWidget(self.main_screen)

    def show_detail_screen(self):
        self.stacked_widget.setCurrentWidget(self.detail_screen)

    def open_detail_window(self, item):
        # Get data of the clicked row
        self.current_row = item.row()
        date = self.past_submissions_screen.past_table.item(self.current_row, 0).text()
        item_type = self.past_submissions_screen.past_table.item(self.current_row, 1).text()
        accomplishment = self.past_submissions_screen.past_table.item(self.current_row, 2).text()
        self.current_item_data = f"Date: {date}, Accomplishment: {accomplishment}"

        # Update the detail view
        self.detail_screen.item_id = self.past_submissions_screen.past_table.item(self.current_row, 0).data(Qt.UserRole)
        self.detail_screen.item_type = item_type 
        self.detail_screen.detail_label.setText(f"Details:\n{self.current_item_data}")
        self.show_detail_screen()

    def refresh_table(self):
        """Refreshes the table to display the latest accomplishments and blockers."""
        accomplishment_data = db_manager.get_accomplishments()
        blocker_data = db_manager.get_blockers()
        row_length = len(blocker_data) + len(accomplishment_data)

        self.past_submissions_screen.past_table.setRowCount(row_length)

        # Populate accomplishments
        for row_idx, (id_, date, accomplishment) in enumerate(accomplishment_data):
            self.past_submissions_screen.past_table.setItem(row_idx, 0, QTableWidgetItem(date))
            self.past_submissions_screen.past_table.setItem(row_idx, 1, QTableWidgetItem("Accomplishment"))
            self.past_submissions_screen.past_table.setItem(row_idx, 2, QTableWidgetItem(accomplishment))

            # Store the ID as hidden data in the first column's item
            self.past_submissions_screen.past_table.item(row_idx, 0).setData(Qt.UserRole, id_)

        # Populate blockers
        for row_idx, (id_, date, blocker) in enumerate(blocker_data):
            row_idx += len(accomplishment_data)
            self.past_submissions_screen.past_table.setItem(row_idx, 0, QTableWidgetItem(date))
            self.past_submissions_screen.past_table.setItem(row_idx, 1, QTableWidgetItem("Blocker"))
            self.past_submissions_screen.past_table.setItem(row_idx, 2, QTableWidgetItem(blocker))

            # Store the ID as hidden data in the first column's item
            self.past_submissions_screen.past_table.item(row_idx, 0).setData(Qt.UserRole, id_)

        # Adjust header and fill empty space
        self.past_submissions_screen.past_table.horizontalHeader().setStretchLastSection(True)
        self.past_submissions_screen.past_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)


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

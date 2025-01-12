from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView
from PyQt5.QtCore import QDate, Qt

class PastSubmissionsScreen(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        """Initializes the past submissions screen layout."""
        self.filter_layout = QHBoxLayout()

        # Date filter inputs
        self.start_date_input = QDateEdit(QDate.currentDate().addYears(-1))
        self.start_date_input.setCalendarPopup(True)
        self.end_date_input = QDateEdit(QDate.currentDate())
        self.end_date_input.setCalendarPopup(True)

        # Filter button
        self.filter_button = QPushButton("Filter")
        self.filter_button.clicked.connect(self.filter_accomplishments)

        # Past accomplishments table
        self.past_table = QTableWidget()
        self.past_table.setColumnCount(3)
        self.past_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.past_table.setSortingEnabled(True)
        self.past_table.setHorizontalHeaderLabels(["Date", "Type", "Details"])

        # Filter layout
        self.filter_layout.addWidget(QLabel("Start Date:"))
        self.filter_layout.addWidget(self.start_date_input)
        self.filter_layout.addWidget(QLabel("End Date:"))
        self.filter_layout.addWidget(self.end_date_input)
        self.filter_layout.addWidget(self.filter_button)

        self.back_button = QPushButton("Back")

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(self.filter_layout)
        layout.addWidget(QLabel("Past Accomplishments:"))
        layout.addWidget(self.past_table)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    def filter_accomplishments(self):
        """Filters accomplishments based on selected date range."""
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        accomplishment_data = self.db_manager.get_accomplishments(start_date, end_date)
        blocker_data = self.db_manager.get_blockers(start_date, end_date)

        combined_data = [
        (id_, date, "Accomplishment", content)
        for id_, date, content in accomplishment_data
        ] + [
        (id_, date, "Blocker", content)
        for id_, date, content in blocker_data
        ]

        self.past_table.setRowCount(len(combined_data))
        for row_idx, (id_, date, item_type, item) in enumerate(combined_data):
            self.past_table.setItem(row_idx, 0, QTableWidgetItem(date))
            self.past_table.setItem(row_idx, 1, QTableWidgetItem(item_type))
            self.past_table.setItem(row_idx, 2, QTableWidgetItem(item))


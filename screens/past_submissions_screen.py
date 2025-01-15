from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QAbstractItemView, QMenu, QAction, QApplication
from PyQt5.QtCore import QDate, Qt
from classes.item import Item

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

    def contextMenuEvent(self, event):
        # Get the position relative to the table
        table_pos = self.past_table.mapFromParent(event.pos())
        selected_rows = set(index.row() for index in self.past_table.selectedIndexes())

        # Adjust for the header height
        table_pos.setY(table_pos.y() - self.past_table.horizontalHeader().height())

        index = self.past_table.indexAt(table_pos)
        if index.isValid():
            isMultiple = len(selected_rows) > 1

            self.menu = QMenu(self)
            copy_action = QAction('Copy', self)
            delete_action = QAction('Delete', self)

            if isMultiple:
                row = selected_rows
                copy_action.triggered.connect(lambda: self.copy_multiple_items(row))
                delete_action.triggered.connect(lambda: self.delete_multiple_items(row))
            else:
                row = index.row()
                copy_action.triggered.connect(lambda: self.copy_item(row))
                delete_action.triggered.connect(lambda: self.delete_item(row))

            self.menu.addAction(copy_action)
            self.menu.addAction(delete_action)
            self.menu.popup(QCursor.pos())
        else:
            return super().contextMenuEvent(event)


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            selected_items = set(index.row() for index in self.past_table.selectedIndexes())
            if len(selected_items) > 1:
                self.delete_multiple_items(selected_items)
            else:
                row = self.past_table.currentRow()
                self.delete_item(row); 
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            selected_items = set(index.row() for index in self.past_table.selectedIndexes())
            if len(selected_items) > 1:
                self.copy_multiple_items(selected_items)
            else:
                row = self.past_table.currentRow()
                self.copyItem(row)
        else:
            super().keyPressEvent(event)
    
    def delete_item(self, row):
        item = Item.from_table_row(self.past_table, row)
        self.past_table.removeRow(row)

        match item.type:
            case "Accomplishment":
                self.db_manager.delete_accomplishment(item.id)
            case "Blocker":
                self.db_manager.delete_blocker(item.id)
            case _:
                return

    def delete_multiple_items(self, row_list):
        #Must track the number of deletions as the row count changes once deleting
        ordered_row_list = sorted(row_list)
        deletion_count = 0
        for row in ordered_row_list:
            row -= deletion_count
            self.delete_item(row)
            deletion_count += 1

    def copy_item(self, row):
        clipboard = QApplication.clipboard()
        clipboard.setText(
        Item.from_table_row(self.past_table, row).getItemCopyString()
        )

    def copy_multiple_items(self, row_list):
        string_to_copy = ''
        for row in row_list:
            string_to_copy += Item.from_table_row(self.past_table, row).getItemCopyString() + '\n'
        clipboard = QApplication.clipboard()
        clipboard.setText(string_to_copy)

        

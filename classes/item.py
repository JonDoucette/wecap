from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

class Item:
    valid_types = ['Accomplishment', 'Blocker']

    def __init__(self, _id, date, _type, comment):
        self._id = _id  # Use private attributes to avoid conflicts with properties
        self._date = date
        self._type = _type
        self._comment = comment

    @classmethod
    def from_table_row(cls, table, row):
        """
        Creates an Item instance from a QTableWidget row.

        Args:
            table (QTableWidget): The table widget containing the data.
            row (int): The index of the row.

        Returns:
            Item: An instance of Item with the data from the table row.
        """
        # Extract data from the row's cells
        _id = table.item(row, 0).data(Qt.UserRole)
        date = table.item(row, 0).text()
        _type = table.item(row, 1).text()
        comment = table.item(row, 2).text()

        # Validate and create an Item instance
        return cls(_id, date, _type, comment)

    def copyItem(self):
        text_to_copy = f"{self._date}\n{self._type}: {self._comment}"

        # Access the clipboard and copy the text
        clipboard = QApplication.clipboard()
        clipboard.setText(text_to_copy)

    def __repr__(self):
        return f"Item(id={self._id}, date='{self._date}', type='{self._type}', comment='{self._comment}')"

    @property
    def id(self):
        return self._id

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, new_date):
        self._date = new_date

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        if new_type not in self.valid_types:
            raise ValueError(f'This is not one of the valid types: {self.valid_types}')
        self._type = new_type

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, new_comment):
        self._comment = new_comment

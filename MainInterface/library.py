import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QListWidget, QListWidgetItem
from pdf import MainWindow
import json
class BookLibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.book_list = QListWidget()
        self.book_list.setViewMode(QListWidget.IconMode) # Set the view mode to IconMode
        self.book_list.setResizeMode(QListWidget.Adjust) # Adjust the size of the icons
        self.book_list.setIconSize(QSize(200, 200)) # Set the icon size
        self.book_list.setWordWrap(True) # Enable word wrap for text
        self.book_list.setTextElideMode(Qt.ElideNone) # Ensure text does not get cut off
        self.layout.addWidget(self.book_list)
        self.load_books()
    def add_book(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Book", "", "PDF Files (*.pdf)")
        if file_name:
            # Assuming the first page of the PDF is the cover
            pixmap = QPixmap(file_name)
            if not pixmap.isNull():
                icon = QIcon(pixmap)
                item = QListWidgetItem(self.book_list)
                item.setIcon(icon)
                # Extract the PDF name from the file path and set it as the text
                item.setText(file_name.split('/')[-1])
                item.setToolTip(file_name)
                self.book_list.addItem(item)
        self.save_books()
    def remove_book(self):
        # Get the currently selected item
        selected_item = self.book_list.currentItem()
        if selected_item:
            # Remove the selected item from the list
            self.book_list.takeItem(self.book_list.row(selected_item))
        self.save_books()
    def open_book(self):
        selected_item = self.book_list.currentItem()
        if selected_item:
            # Retrieve the path from the tooltip of the selected item
            path = selected_item.toolTip()
            # Now you can use the path to open the book
            pdf = MainWindow(path=path)
            pdf.show()
    def save_books(self):
        books = [item.toolTip() for item in self.book_list.findItems("", Qt.MatchContains)]
        with open('books.json', 'w') as f:
            json.dump(books, f)
    def load_books(self):
        try:
            with open('books.json', 'r') as f:
                books = json.load(f)
                for book in books:
                    self.add_book_from_path(book)
        except FileNotFoundError:
            pass
    def add_book_from_path(self, path):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            icon = QIcon(pixmap)
            item = QListWidgetItem(self.book_list)
            item.setIcon(icon)
            item.setText(path.split('/')[-1])
            item.setToolTip(path)
            self.book_list.addItem(item)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookLibraryApp()
    window.show()
    sys.exit(app.exec())
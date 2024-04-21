from PySide6 import QtWidgets,QtCore
import os

class Data_Bookmark:
    
    def __init__(self, bookmark_name, page_number, notes,word):
        self.bookmark_name = bookmark_name
        self.page_number = page_number
        self.notes = notes
        self.word=word

class MyWindow(QtWidgets.QWidget):
    def __init__(self, page_number,pdf_name,current_dir,word):
        super().__init__()
        self.page_number = page_number
        self.pdf_name=pdf_name
        self.current_dir=current_dir
        self.word=word
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Bookmark Manager")

        # Create QTableWidget with 3 columns for name, page number, and notes
        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Bookmark Name", "Page Number", "Notes","Hint"])

                # Set the size policy for the table widget
        self.table_widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
                # Set selection mode to select entire rows
        self.table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # Set the size of the columns
        self.table_widget.setColumnWidth(0, 150)  # Bookmark Name
        self.table_widget.setColumnWidth(1, 80)  # Page Number
        self.table_widget.setColumnWidth(2, 250)  # Notes
        self.table_widget.setColumnWidth(3, 250)  # Hint

        # Set the row height for better visibility of multi-line notes
        self.table_widget.verticalHeader().setDefaultSectionSize(50)

        # Create QPushButton for adding, editing, and removing bookmarks
        self.add_button = QtWidgets.QPushButton("Add Bookmark", self)
        self.add_button.clicked.connect(self.add_bookmark)

        self.edit_button = QtWidgets.QPushButton("Edit Bookmark", self)
        self.edit_button.clicked.connect(self.edit_bookmark)

        self.remove_button = QtWidgets.QPushButton("Remove Bookmark", self)
        self.remove_button.clicked.connect(self.remove_bookmark)

        self.close_button = QtWidgets.QPushButton("Close",self)
        self.close_button.clicked.connect(self.close)



        # Create layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.add_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.close_button)

        # Load bookmarks from file
        self.load_bookmarks()


    def add_bookmark(self):
        # Simulate getting bookmark data (name, page number, notes) from user input
        bookmark_name, ok = QtWidgets.QInputDialog.getText(self, "Input Dialog", "Enter Bookmark name:")
        if not ok:
            return
        
        notes, ok = QtWidgets.QInputDialog.getText(self, "Input Dialog", "Enter notes:")
        if not ok:
            return

        # Create bookmark object
        bookmark = Data_Bookmark(bookmark_name, self.page_number, notes,self.word)

        # Add bookmark to the table
        self.add_bookmark_to_table(bookmark)

        # Save bookmarks to file
        self.save_bookmarks()

    def edit_bookmark(self):
        # Get selected item
        selected_item = self.table_widget.selectedItems()
        if not selected_item:
            return

        row = selected_item[0].row()

        # Retrieve bookmark details from the selected row
        bookmark_name = self.table_widget.item(row, 0).text()
        notes = self.table_widget.item(row, 2).text()

        # Prompt user to edit bookmark details
        new_bookmark_name, ok = QtWidgets.QInputDialog.getText(self, "Edit Bookmark", "Enter new bookmark name:", text=bookmark_name)
        if not ok:
            return

        new_notes, ok = QtWidgets.QInputDialog.getText(self, "Edit Bookmark", "Enter new notes:", text=notes)
        if not ok:
            return

        # Update bookmark details in the table
        self.table_widget.item(row, 0).setText(new_bookmark_name)
        self.table_widget.item(row, 2).setText(new_notes)

        # Save bookmarks to file
        self.save_bookmarks()

    def remove_bookmark(self):
        
        # Get selected item
        selected_item = self.table_widget.selectedItems()
        if not selected_item:
            return

        row = selected_item[0].row()

        # Remove selected row from the table
        self.table_widget.removeRow(row)

        # Save bookmarks to file
        self.save_bookmarks()

    def add_bookmark_to_table(self, bookmark):

        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        # Insert bookmark's details into the table
        self.table_widget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(bookmark.bookmark_name))
        self.table_widget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(bookmark.page_number)))
        self.table_widget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(bookmark.notes))
        self.table_widget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(bookmark.word))

    def save_bookmarks(self):
        # Define the file name based on the PDF name
        filename = f"{self.pdf_name}_bookmarks.txt"
        # Get the current directory
        filepath = os.path.join(self.current_dir, filename)
        # Open the file in write mode
        with open(filepath, "w",encoding="utf-8") as file:
            # Write all bookmarks to the file
            for row in range(self.table_widget.rowCount()):
                bookmark_name = self.table_widget.item(row, 0).text()
                page_number = int(self.table_widget.item(row, 1).text())
                notes = self.table_widget.item(row, 2).text().replace('\n', '<br>')  # Replace newline with a placeholder
                word = self.table_widget.item(row, 3).text().replace('\n', '<br>')  # Replace newline with a placeholder
                file.write(f"{bookmark_name};{page_number};{notes};{word}\n")

    def load_bookmarks(self):
        # Define the file name based on the PDF name
        filename = f"{self.pdf_name}_bookmarks.txt"
        # Get the current directory
        filepath = os.path.join(self.current_dir, filename)
        # Open the file in read mode
        try:
            with open(filepath, "r+",encoding="utf-8") as file:
                # Read each line from the file
                for line in file:
                    # Split the line into bookmark details
                    bookmark_name, page_number, notes,word = line.strip().split(';')
                    page_number = int(page_number)
                    # Replace placeholder with newline character
                    notes = notes.replace('<br>', '\n')
                    word = word.replace('<br>', '\n')
                    # Create bookmark object
                    bookmark = Data_Bookmark(bookmark_name, page_number, notes, word)
                    # Add bookmark to the table
                    self.add_bookmark_to_table(bookmark)

        except FileNotFoundError:
            # If the file doesn't exist, create it
            with open(filepath, "w", encoding="utf-8"):
                pass  # Do nothing, file created




        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWindow(1, "test", ".",'l')  # Pass the page number, PDF name, and current directory as arguments
    window.setGeometry(100, 100, 400, 300)
    window.show()
    app.exec()

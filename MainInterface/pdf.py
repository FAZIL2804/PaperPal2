import sys,os
from add_bookmark import MyWindow
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QTextEdit,
    QLineEdit,
    QSlider,#
    QDialog,QTableWidget,QTableWidgetItem,
    QAbstractItemView  #
)
from PySide6.QtCore import Qt, QTimer # Added QTextCursor import
import fitz
import extra_functions
from PySide6 import QtGui,QtWidgets
from PySide6.QtGui import QTextBlockFormat, QFont, QTextCursor 

class CustomButton(QPushButton):
    def __init__(self, label):
        super().__init__()
        font = QFont()
        font.setFamilies([u"JetBrains Mono NL"])
        font.setBold(True)
        self.setFont(font)
        self.setText(label)
        self.setFixedSize(160, 40)# Adjust the size as needed
        self.setStyleSheet("""
            QPushButton {
                background-color:  #353535;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #282828;
            }
            QPushButton:pressed {
                background-color: #4c4c4c;
            }
        """)

class CustomButton_2(QPushButton):
    def __init__(self, label):
        super().__init__()
        font = QFont()
        font.setFamilies([u"JetBrains Mono NL"])
        font.setBold(True)
        self.setFont(font)
        self.setText(label)
        self.setFixedSize(160, 80)  # Adjust the size as needed
        self.setStyleSheet("""
            QPushButton {
                background-color:  #353535;
                color: white;
                border: none;
                border-radius: 5px;
                text-align: center; /* Center align text */
            }
            QPushButton:hover {
                background-color: #282828;
            }
            QPushButton:pressed {
                background-color: #4c4c4c;
            }
        """)



class PDFView(QWidget):
    def __init__(self, path):
        super().__init__()
        self.pdf_path = path
        self.text_edit = QTextEdit()
        self.extract_text()
        self.setup_ui()

    def extract_text(self):
        doc = fitz.open(self.pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        self.text_edit.setPlainText(text)
        # Center align the text
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignCenter)
        cursor.mergeBlockFormat(block_format)
        self.text_edit.setTextCursor(cursor)
        # Set cursor position to the beginning of the text
        self.text_edit.moveCursor(QtGui.QTextCursor.Start)

    def setup_ui(self):
        self.text_edit.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)

    def get_selected_text(self):
        return self.text_edit.textCursor().selectedText()


class InfoLabel(QWidget):
    def __init__(self):
        super().__init__()
        self.information = QLabel("Info Appears here")
        self.information.setMaximumHeight(100)
        self.information.setStyleSheet("""background-color:#d7d7d7;
                                         border-radius: 15px;
                                       """)

    def print_data(self, message):
        self.information.setText(message)


class ButtonHolder(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.stored_signal=None

        self.meaning_button = CustomButton("Meaning")
        self.meaning_button.clicked.connect(self.on_meaning_button_clicked)

        self.synonym_button = CustomButton("Synonym")
        self.synonym_button.clicked.connect(self.on_synonym_button_clicked)

        self.speech_button = CustomButton("Read Aloud")
        self.speech_button.clicked.connect(self.on_speech_button_clicked)
        
        self.auto_scroll_button = CustomButton("Auto-Scroll")
        self.auto_scroll_button.setCheckable(True)
        self.auto_scroll_button.toggled.connect(self.on_auto_scroll_toggled)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(5)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setMaximumWidth(120)  # Set maximum width to match button
        self.speed_slider.valueChanged.connect(self.on_speed_changed)

        self.close_button = CustomButton("Close")
        self.close_button.clicked.connect(self.main_window.close)
        font = QFont()
        font.setFamilies([u"JetBrains Mono NL"])
        font.setBold(True)
        self.autoscroll_label = QLabel("Auto-Scroll Speed:")
        self.autoscroll_label.setStyleSheet("""color:#ffffff;
                                            font-size: 8pt;""")
        self.autoscroll_label.setFont(font)
        
        self.search_label = QLabel("Search:")
        self.search_box = QLineEdit()
        self.search_button = CustomButton("Search")
        self.search_button.clicked.connect(self.search_pdf)

        self.next_button = CustomButton(">")
        self.next_button.clicked.connect(self.next_occurrence)
        self.next_button.setFixedSize(60,40)

        self.prev_button = CustomButton("<")
        self.prev_button.clicked.connect(self.prev_occurrence)
        self.prev_button.setFixedSize(60,40)

        self.add_bookmark_button = CustomButton_2("Bookmarks \n (Select a text )") 
        self.add_bookmark_button.clicked.connect(self.add_bookmark)

        self.go_to_bookmark_button= CustomButton("Go to Bookmark")
        self.go_to_bookmark_button.clicked.connect(self.go_to_bookmark)

        self.navigate_layout=QHBoxLayout()
        self.navigate_layout.addWidget(self.prev_button)
        self.navigate_layout.addWidget(self.next_button)

        self.search_results = []
        self.search_result=[]
        self.current_pos = -1
        self.container = QVBoxLayout()
        self.container.addWidget(self.meaning_button)
        self.container.addWidget(self.synonym_button)
        self.container.addWidget(self.speech_button)
        self.container.addWidget(self.auto_scroll_button)
        self.container.addWidget(self.autoscroll_label)
        self.container.addWidget(self.speed_slider)
        self.container.addWidget(self.search_label)
        self.container.addWidget(self.search_box)
        self.container.addWidget(self.search_button)
        self.container.addLayout(self.navigate_layout)
        self.container.addWidget(self.add_bookmark_button)
        self.container.addWidget(self.go_to_bookmark_button)
        self.container.addWidget(self.close_button)
        self.container.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.container)

    def on_meaning_button_clicked(self):
        selected_text = self.main_window.pdf_view.get_selected_text()
        if selected_text:
            definition = extra_functions.get_definition(selected_text)
            self.main_window.information.print_data(f"Meaning of {selected_text} : {definition}")

    def on_synonym_button_clicked(self):
        selected_text = self.main_window.pdf_view.get_selected_text()
        if selected_text:
            synonyms = extra_functions.get_synonyms(selected_text)
            if synonyms:
                self.main_window.information.print_data(f"Synonym of {selected_text} : {synonyms[0]}")

    def on_speech_button_clicked(self):
        selected_text = self.main_window.pdf_view.get_selected_text()
        if selected_text:
            extra_functions.get_word_pronunciation(selected_text)

    def on_auto_scroll_toggled(self, checked):
        if checked:
            self.main_window.start_auto_scroll()
        else:
            self.main_window.stop_auto_scroll()

    def on_speed_changed(self, value):
        self.main_window.set_auto_scroll_speed(value)


    def search_pdf(self):
        search_query = self.search_box.text()
        print(search_query,type(search_query))
        if search_query:
            # Set the cursor to the start of the document
            cursor = self.main_window.pdf_view.text_edit.textCursor()
            cursor.setPosition(0)
            self.main_window.pdf_view.text_edit.setTextCursor(cursor)
            
            # Clear previous search results
            self.search_results.clear()
            self.current_pos = -1
            
            # Search for all occurrences of the word
            while True:
                found_cursor = self.main_window.pdf_view.text_edit.document().find(search_query, cursor)
                if found_cursor.isNull():
                    break
                self.search_results.append(found_cursor)
                cursor = found_cursor

            if self.search_results:
                # Move the cursor to the first occurrence
                self.current_pos = 0
                self.main_window.pdf_view.text_edit.setTextCursor(self.search_results[self.current_pos])
                # Ensure the found word is visible
                self.main_window.pdf_view.text_edit.ensureCursorVisible()
            else:
                self.main_window.information.print_data("Search query not found.")

    def next_occurrence(self):
        if self.search_results:
            self.current_pos = (self.current_pos + 1) % len(self.search_results)
            print(self.current_pos)
            self.main_window.pdf_view.text_edit.setTextCursor(self.search_results[self.current_pos])
            self.main_window.pdf_view.text_edit.ensureCursorVisible()

    
   
    def prev_occurrence(self):
        if self.search_results:
            self.current_pos = (self.current_pos - 1) % len(self.search_results)
            self.main_window.pdf_view.text_edit.setTextCursor(self.search_results[self.current_pos])
            self.main_window.pdf_view.text_edit.ensureCursorVisible()


    def add_bookmark(self):

        selected_text = self.main_window.pdf_view.get_selected_text()
        if selected_text:
            # Get the current page number based on the cursor position
            cursor = self.main_window.pdf_view.text_edit.textCursor()
            current_page = cursor.blockNumber() + 1 
            current_dir = os.getcwd()   
            pdf_name=os.path.splitext(os.path.basename(self.main_window.pdf_view.pdf_path))[0]
            bookmark_window = MyWindow(current_page,pdf_name,current_dir,selected_text)  # This creates the window for adding a bookmark
            bookmark_window.setGeometry(100, 100, 900, 400)  # Adjust geometry as needed
            bookmark_window.show()  # Show the window

            # Call exec_ to ensure the application event loop is properly executed
            bookmark_window.exec()
        else:
            QMessageBox.information(self,"No Text selected "," please select a text to add bookmark")

    def go_to_bookmark(self):
        current_dir = os.getcwd()   
        pdf_name=os.path.splitext(os.path.basename(self.main_window.pdf_view.pdf_path))[0]
        dialog=open_bookmark(pdf_name,current_dir)
        result = dialog.exec()
        if result == QDialog.Accepted:
             selected_page_number,selected_word = dialog.get_selected_bookmark()
             if selected_page_number is not None:
                 self.search_bookmark(selected_page_number,selected_word)

    def search_bookmark(self, page_number, word):

        if word:
            # Set the cursor to the start of the document
            cursor = self.main_window.pdf_view.text_edit.textCursor()
            cursor.setPosition(0)
            self.main_window.pdf_view.text_edit.setTextCursor(cursor)
            
            # Clear previous search results
            self.search_result.clear()
            self.current_pos = -1
            while True:
                found_cursor = self.main_window.pdf_view.text_edit.document().find(word, cursor)
                if found_cursor.isNull():
                    break
                self.search_result.append(found_cursor)
                cursor = found_cursor
            
            # Search for all occurrences of the word
            if self.search_result:
                     self.current_pos=0
                # Move the cursor to the first occurrence
                     new_cursor = self.main_window.pdf_view.text_edit.textCursor()
                     current_page = new_cursor.blockNumber() + 1
                     while (current_page!=page_number) :
                              self.current_pos = (self.current_pos + 1) % len(self.search_result)
                              self.main_window.pdf_view.text_edit.setTextCursor(self.search_result[self.current_pos])
                              self.main_window.pdf_view.text_edit.ensureCursorVisible()
                              cursor = self.main_window.pdf_view.text_edit.textCursor()
                              current_page = cursor.blockNumber() + 1
            else:
                self.main_window.information.print_data("Bookmark not found.")

class Data_Bookmark:
    def __init__(self, bookmark_name, page_number, notes,word):
        self.bookmark_name = bookmark_name
        self.page_number = page_number
        self.notes = notes
        self.word=word

class open_bookmark(QDialog):
    def __init__(self, pdf_name, current_dir):
        super().__init__()
        self.pdf_name = pdf_name
        self.current_dir = current_dir
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Open Bookmark")

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Bookmark Name", "Page Number", "Notes"])

        self.table_widget.setColumnWidth(0, 150)  # Bookmark Name
        self.table_widget.setColumnWidth(1, 80)  # Page Number
        self.table_widget.setColumnWidth(2, 250)  # Notes
        self.table_widget.setColumnWidth(3, 250)  # Hint

        # Set the row height for better visibility of multi-line notes
        self.table_widget.verticalHeader().setDefaultSectionSize(50)

        # Set selection mode to select entire rows
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.open_button = QPushButton("Open Bookmark", self)
        self.open_button.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.open_button)

        self.load_bookmarks()
        self.setFixedSize(900, 400)

    def add_bookmark_to_table(self, bookmark):

        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        # Insert bookmark's details into the table
        self.table_widget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(bookmark.bookmark_name))
        self.table_widget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(bookmark.page_number)))
        self.table_widget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(bookmark.notes))
        self.table_widget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(bookmark.word))

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


    def get_selected_bookmark(self):
        selected_items = self.table_widget.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            page_number = int(self.table_widget.item(row, 1).text())
            word = self.table_widget.item(row, 3).text().split()
            return [page_number,word[0]]
        return None


    

class MainWindow(QWidget):


    def __init__(self, path):
        super().__init__()
        self.setWindowTitle("PySide6 PDF Viewer")
        self.pdf_view = PDFView(path)
        self.information = InfoLabel()
        self.button_holder = ButtonHolder(self)

            

        self.qlayout = QVBoxLayout()
        self.qlayout.addWidget(self.pdf_view.text_edit, 10)
        self.qlayout.addWidget(self.information.information, 1)
        self.hlayout = QHBoxLayout()
        self.hlayout.addLayout(self.qlayout, 10)
        self.hlayout.addWidget(self.button_holder, 1)
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hlayout)

        self.setWindowState(Qt.WindowFullScreen)
        self.setStyleSheet("""
            QWidget#pdf_view{
                background-color:#e0e0e0;
                color-black;
            }
            QWidget{
                background-color:#333333;
            }              
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
            }
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color:  #353535;
                border: 1px solid black;             
                padding: 10px;
            }
            QPushButton:hover {
                background-color:#282828;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
        """)

        # Initialize QTimer for auto-scroll
        self.auto_scroll_timer = QTimer(self)
        self.auto_scroll_timer.timeout.connect(self.auto_scroll)
        self.auto_scroll_speed = 50  # Default auto-scroll speed
        self.is_auto_scrolling = False

    def start_auto_scroll(self):
        self.is_auto_scrolling = True
        self.auto_scroll_timer.start(1000 // self.auto_scroll_speed)

    def stop_auto_scroll(self):
        self.is_auto_scrolling = False
        self.auto_scroll_timer.stop()

    def set_auto_scroll_speed(self, speed):
        self.auto_scroll_speed = speed * 10
        if self.is_auto_scrolling:
            self.auto_scroll_timer.setInterval(1000 // speed)

    def auto_scroll(self):
        # Calculate the maximum scroll position
        max_scroll = self.pdf_view.text_edit.verticalScrollBar().maximum()
        # Increment scroll position
        current_scroll = self.pdf_view.text_edit.verticalScrollBar().value()
        new_scroll = current_scroll + 1
        if new_scroll > max_scroll:
            new_scroll = 0
        # Set new scroll position
        self.pdf_view.text_edit.verticalScrollBar().setValue(new_scroll)



    




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("test.pdf")
    window.show()
    sys.exit(app.exec())
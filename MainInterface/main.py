from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget,QVBoxLayout,QSpacerItem,QHBoxLayout)
import sys
from library import BookLibraryApp
class Buttons(QPushButton):
    def __init__(self, label):
        super().__init__()
        font1 = QFont()
        font1.setFamilies([u"JetBrains Mono NL"])
        font1.setBold(True)
        self.setFont(font1)
        self.setText(label)
        self.setFixedSize(131, 32)
        self.setStyleSheet("""
            QPushButton {
                background-color:  #353535;
                color:white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color:#282828;
            }
            QPushButton:pressed {
                background-color: #4c4c4c;
            }
        """)
class ButtonHolder(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.addBook_button = Buttons("ADD BOOK")
        self.removeBook_button = Buttons("REMOVE")
        self.openbook_button = Buttons("OPEN")
        self.summarizeBook_button = Buttons("SUMMARIZE")
        self.close_button = Buttons("CLOSE")
        self.main_window = main_window
        self.setup_ui()
        self.addBook_button.clicked.connect(self.add_button_clicked)
        self.removeBook_button.clicked.connect(self.remove_button_clicked)
        self.openbook_button.clicked.connect(self.open_button_clicked)
        self.close_button.clicked.connect(self.close_button_clicked)
    def add_button_clicked(self):
        self.main_window.library_widget.add_book()
    def close_button_clicked(self):
        self.main_window.close()
    def remove_button_clicked(self):
        self.main_window.library_widget.remove_book()
    def open_button_clicked(self):
        self.main_window.library_widget.open_book()
    def setup_ui(self):
        self.v_layout = QVBoxLayout()
        self.v_layout.addItem(QSpacerItem(0, 250, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.v_layout.setSpacing(20)
        self.v_layout.addWidget(self.addBook_button)
        self.v_layout.addWidget(self.removeBook_button)
        self.v_layout.addWidget(self.openbook_button)
        self.v_layout.addWidget(self.summarizeBook_button)
        self.v_layout.addWidget(self.close_button)
        self.v_layout.addItem(QSpacerItem(0, 250, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.v_layout)
class SubHeadingLabel(QLabel):
    def __init__(self, label):
        super().__init__()
        self.setGeometry(QRect(10, 10, 201, 41))
        font = QFont()
        font.setFamilies([u"JetBrains Mono ExtraBold"])
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.setFont(font)
        self.setText(label)
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 400)
        self.subheading_label = SubHeadingLabel("Your Library")
        self.buttons_container = ButtonHolder(self)
        self.library_widget = BookLibraryApp()
        self.setup_ui()
        
    def setup_ui(self):
        app = QApplication.instance()
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(42, 42, 42))
        palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.subheading_label)
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vertical_layout.addItem(spacer)
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.library_widget)
        self.horizontal_layout.addWidget(self.buttons_container)
        self.vertical_layout.addLayout(self.horizontal_layout)
        self.setLayout(self.vertical_layout)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



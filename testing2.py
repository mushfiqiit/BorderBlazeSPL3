import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QGridLayout, QPushButton
)
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import QSize, Qt

class Color(QWidget):
    def __init__(self, color):
        super(Color,self).__init__()
        self.setAutoFillBackground(True)

        palette=self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QWidget):

    def __init__(self,color):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App")
        self.setContentsMargins(20,20,20,20)
        self.setAutoFillBackground(True)

        palette=self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

        layout=QGridLayout()
        self.setLayout(layout)

        title=QLabel("Point Cloud Boundary Detector")
        title.setFont(QFont("Calibri", 24))
        layout.addWidget(title, 0,1,1,1)

        uploadDialog=QLabel("Upload your point cloud data here ")
        uploadDialog.setFont(QFont("Calibri", 16))
        layout.addWidget(uploadDialog, 1,1)

        uploadButton=QPushButton("Upload")
        layout.addWidget(uploadButton, 1,2,1,1)

        layout.addWidget(QLabel(), 2,0)

        description=QLabel("Choose a method")
        description.setFont(QFont("Calibri", 16))
        layout.addWidget(description, 3,1,2,3)


app=QApplication(sys.argv)

app.setStyleSheet("""
    QWidget {
        background-color: "green";
        color: "white";
    }

    QLineEdit {
        
    }
""")

w=MainWindow('mintcream')
w.show()
app.exec()
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Boundary Detection Tool")
        layout=QVBoxLayout()
        headline=QLabel("Point Cloud Boundary Detector")
        widgets=[headline]
        for widget in widgets:
            layout.addWidget(widget)
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(container)

app=QApplication(sys.argv)
w=MainWindow()
w.show()
app.exec()
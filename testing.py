import sys
import os
import platform
import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import pyqtgraph.opengl as gl

# ==> MAIN WINDOW
from GUI.GUI import Ui_MainWindow
from GUI.ui_splash_screen import Ui_SplashScreen

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

app=QApplication(sys.argv)
w=MainWindow()
w.show()
app.exec()
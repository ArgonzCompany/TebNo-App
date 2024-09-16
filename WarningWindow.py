from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui, QtCore
from TebnoWarning import Ui_TebNoProduct

class WarningWindow(QWidget, Ui_TebNoProduct):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("طبنو")
        self.setWindowIcon(QtGui.QIcon(':/images/TebNoLogo.png'))
        self.show()
    
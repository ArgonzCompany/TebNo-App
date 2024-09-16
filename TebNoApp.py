from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtGui, QtCore
from TebNo import Ui_TebNoContainer
from database import TableHandling
from OSHandling import OSHandling


class TebNoWindow(QWidget, Ui_TebNoContainer):
    
    def __init__(self):
        super().__init__()
        # TableHandling.tablesCreating()
        self.setupUi(self)
        self.nationalCode.installEventFilter(self)
        self.phoneNumber.installEventFilter(self)
        self.birthDate.installEventFilter(self)
        self.setWindowTitle("طبنو")
        self.setWindowIcon(QtGui.QIcon(':/images/TebNoLogo.png'))
        self.show()
    
    def eventFilter(self, source, event):
        
        if event.type() == QtCore.QEvent.MouseButtonPress:

            if source == self.nationalCode:
                self.nationalCode.setFocus(QtCore.Qt.MouseFocusReason)
                self.nationalCode.setCursorPosition(0)
                return True
            if source == self.phoneNumber:
                self.phoneNumber.setFocus(QtCore.Qt.MouseFocusReason)
                self.phoneNumber.setCursorPosition(0)
                return True
            
            if source == self.birthDate:
                self.birthDate.setFocus(QtCore.Qt.MouseFocusReason)
                self.birthDate.setCursorPosition(1)
                return True

        return super().eventFilter(source, event)





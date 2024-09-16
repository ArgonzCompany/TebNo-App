
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtGui, QtCore
import sys
from ConfirmWindow import ConfirmWindow
from WarningWindow import WarningWindow
from TebNoApp import TebNoWindow
from OSHandling import OSHandling
from TimerBox import TimerMessageBox
from database import TableHandling

if __name__ == "__main__":

     TableHandling.tablesCreating()
     app = QApplication(sys.argv)
     
     # these lines of codes are used for application authentication
     # confirm = ConfirmWindow()
     
     #app without authentication
     Tebnoapp = TebNoWindow()
     sys.exit(app.exec())
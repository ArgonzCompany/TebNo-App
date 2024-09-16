
from PyQt5.QtWidgets import  QMessageBox
from PyQt5 import QtCore, QtGui
from pathlib import Path
import os
from OSHandling import OSHandling

class TimerMessageBox(QMessageBox):

    def __init__(self, timeout=3, message=None, font=None, parent=None):
        super(TimerMessageBox, self).__init__(parent)
        self.setFont(font)
        self.setObjectName("TimerBoxStyle")
        #Style Path
        with open(OSHandling.messageboxHandling(), 'r') as f:
            self.setStyleSheet(f.read())
        self.setWindowTitle("پیام به کاربر")
        self.setWindowIcon(QtGui.QIcon(':/images/TebNoLogo.png'))
        self.time_to_wait = timeout
        self.setText(message)
        self.setIcon(QMessageBox.Information)
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeStatus)
        self.timer.start()
    
    def changeStatus(self):
        self.time_to_wait -=1
        if (self.time_to_wait) <=0:
            self.close()
    
    def closeEvent(self, event):
        self.timer.stop()
        event.accept()
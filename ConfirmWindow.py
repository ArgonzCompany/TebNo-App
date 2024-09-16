from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtGui, QtCore
import sys
from TebNoConfirm import Ui_TebnoConfirmation
import requests
import json
from OSHandling import OSHandling
from TimerBox import TimerMessageBox
from TebNoApp import TebNoWindow
import resources
from database import  TableHandling
from WarningWindow import WarningWindow

class ConfirmWindow(QWidget, Ui_TebnoConfirmation):
    
    def __init__(self):
        
        #TableHandling.tablesCreating()
        super().__init__()
        QtGui.QFontDatabase.addApplicationFont(':/fonts/Vazirmatn-Bold.ttf')
        self.font = QtGui.QFont()
        self.font.setFamily("Vazirmatn")
        self.font.setPointSize(12)
        self.setupUi(self)
        self.setWindowTitle("طبنو")
        self.setWindowIcon(QtGui.QIcon(':/images/TebNoLogo.png'))
        self.url = "https://argonz.ir/wp-json/tebno/v2/user"
        self.submitBtnConfirm.clicked.connect(self.doAuthentication)
        self.show()
    
    
    
    
    def doAuthentication(self):
 
        headers = {"Content-Type": "application/json; charset=utf-8"}
        
        data = {
            "name": self.name.text(),
            "lastname": self.fname.text(),
            "phoneNumber": self.phoneNumber.text(),
            "mac_address": OSHandling.get_mac_address(),
        }
        
        timeout = 5
        try:
            response = requests.post(self.url, headers=headers, json=data, timeout=timeout)
            message = response.json()["message"]

            if(message == "کاربر موجود است"):
                self.message_alert = TimerMessageBox(2, "شما مجوز لازم برای ورود را دارید.", self.font)
                self.message_alert.exec_()
                self.close()
                self.tebno = TebNoWindow()
            if(message == "شما مجوز ندارید"):
                self.message_alert = TimerMessageBox(2, "شما مجوز لازم برای ورود را ندارید.", self.font)
                self.message_alert.exec_()
                self.close()
            if(message == "استفاده غیر قانونی"):
                self.close()
                self.warning = WarningWindow()
        
        except(requests.ConnectionError, requests.Timeout) as exception:
            self.message_alert = TimerMessageBox(4, "اتصال اینترنت شما قطع است. برای هویت سنجی نیاز است.", self.font)
            self.message_alert.exec_()
               
    
    def closeEvent(self, event):
        event.accept()

                        




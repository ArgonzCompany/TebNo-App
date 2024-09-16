from database import VisitOperations
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtCore, QtGui
from VisitDialog import Ui_visitDialog
from TimerBox import TimerMessageBox
from VisitModel import VisitModel
from AllVisits import AllVisitsModel
from unidecode import unidecode

class VisitWindow(QWidget, Ui_visitDialog):
    closed = QtCore.pyqtSignal()
    def __init__(self, patient_ncode):
        super().__init__()
        self.setupUi(self)
        self.visit_id = None
        self.patient_ncode = patient_ncode
        self.visitsList = None
        self.visitsMain = None
        self.setWindowTitle("طبنو")
        self.setWindowIcon(QtGui.QIcon(':/images/TebNoLogo.png'))
        self.visitEditBtn.clicked.connect(self.visitEdition)

    
    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
    
    def setScreen(self):
        visit_data = VisitOperations.show_visit(self.visit_id)
       
        if(visit_data is not None):

            if(visit_data.get('visitStatus') == "نامشخص"):
                self.visitStatus.clear()
                self.visitStatus.addItems(["نامشخص", "تایید شده", "لغو شده"])
                self.visitHour.setText(visit_data.get('visitHour'))
                self.visitDate.setText(visit_data.get('visitDate'))
                self.visitDescription.setPlainText(visit_data.get('visitDescription'))
            
            if(visit_data.get('visitStatus') == "تایید شده"):
                self.visitStatus.clear()
                self.visitStatus.addItem("تایید شده")
                self.visitStatus.setEnabled(False)
                self.visitHour.setText(visit_data.get('visitHour'))
                self.visitHour.setReadOnly(True)
                self.visitDate.setText(visit_data.get('visitDate'))
                self.visitDate.setReadOnly(True)
                self.visitDescription.setPlainText(visit_data.get('visitDescription'))

            #self.visitEditBtn.clicked.connect(self.visitEdition)
    
    def visitEdition(self):

            args = {
                'status': self.visitStatus.currentText(),
                'visit_hour': unidecode(self.visitHour.text()),
                'visit_date': unidecode(self.visitDate.text()),
                'description': self.visitDescription.toPlainText()
            }

                
            message = VisitOperations.editVisit(self.visit_id, **args)
            if message == "به روز رسانی انجام شد.":
                self.visitsList.setModel(VisitModel(self, ['شناسه', 'تاریخ', 'ساعت', 'وضعیت'], self.patient_ncode ))
                self.visitsMain.setModel(AllVisitsModel(self, ['نام خانوادگی', 'کد ملی','تاریخ', 'ساعت', 'وضعیت']))
            self.message_alert = TimerMessageBox(3, message, self.font)
            self.message_alert.exec_()
            self.close()
    
            
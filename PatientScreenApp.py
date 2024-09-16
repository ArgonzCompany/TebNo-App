from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5 import QtCore, QtWidgets, QtGui
from PatientScreen import Ui_patientInfo 
from database import PatientOperations, VisitOperations
from PatientModel import PatientModel
from AllVisits import AllVisitsModel
from VisitModel import VisitModel
from VisitDialogApp import VisitWindow
from pathlib import Path
from TimerBox import TimerMessageBox
from unidecode import unidecode
from CreateReport import CreateReport
import jdatetime as jd

class PatientWindow(QWidget, Ui_patientInfo):
    closed = QtCore.pyqtSignal()
    def __init__(self, visitsList, nationalCode, patientsList):
        super().__init__()
        self.setupUi(self)
        self.patient_ncode = nationalCode
        self.patient_scr = None
        self.patientsList = patientsList
        self.visitsMain = visitsList
        #visit dialog
        self.visitDialog = VisitWindow(self.patient_ncode)
        # self.visitDialog.closed.connect(self.show)
        self.visitsList.doubleClicked.connect(self.visitsShow)
        self.editPatient.clicked.connect(self.edit_patient)
        self.deletePatient.clicked.connect(self.delete_patient)
        self.visitBtn.clicked.connect(self.addVisit)
        self.patientInfoBtn.clicked.connect(self.createFile)
        self.setWindowTitle("طبنو")
        self.setWindowIcon(QtGui.QIcon(':/images/TebNoLogo.png'))
        self.visitDate.installEventFilter(self)
        self.visitTime.installEventFilter(self)

    def closeEvent(self, event):
        self.closed.emit()

    
    def edit_patient(self):
        
        self.messagebox = QMessageBox()
        self.messagebox.setIcon(QMessageBox.Question)
        self.messagebox.setWindowIcon(QtGui.QIcon(':/images/TebNoLogo.png'))
        self.messagebox.setWindowTitle("ویرایش بیمار")
        self.messagebox.setFont(self.font)
        self.messagebox.setText("آیا از ویرایش بیمار مورد نظر مطمئن هستید؟")
        # self.messagebox.addButton(QMessageBox.Yes)
        self.messagebox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        self.messagebox.button(QMessageBox.Yes).setText('بلی')
        self.messagebox.button(QMessageBox.No).setText('خیر')
        result = self.messagebox.exec_()

        args = {
            'name': self.name.text(),
            'lastname': self.fname.text(),
            'birth_date': unidecode(self.birth.text()),
            'phoneNumber': unidecode(self.phoneNumber.text()),
            'nationalCode': unidecode(self.nationalCode.text()),
            'patient_ncode': self.patient_ncode 
        }
        
        if(result == QMessageBox.Yes):
            message = PatientOperations.editPatient(**args)
            if (message == "به روز رسانی انجام شد."):
                self.patientsList.setModel(PatientModel(self, ['نام','نام خانوادگی', 'کد ملی', 'شماره همراه']))
                self.visitsMain.setModel(AllVisitsModel(self, ['نام خانوادگی', 'کد ملی','تاریخ', 'ساعت', 'وضعیت']))
            self.message_alert = TimerMessageBox(3, message, self.font)
            self.message_alert.exec_()
            self.close()
        
        

    
    def setScreen(self):
        self.patient_scr = PatientOperations.show_patient(self.patient_ncode)
        self.name.setText(self.patient_scr.name)
        self.fname.setText(self.patient_scr.lastname)
        self.phoneNumber.setText(self.patient_scr.phoneNumber)
        self.nationalCode.setText(self.patient_scr.nationalCode)
        self.birth.setText(self.setDatetoJalali(self.patient_scr.birth_date))
        self.setVisitsListInfo()
    
    def setDatetoJalali(self,date):
        date_type=jd.date.fromgregorian(day=date.day, month=date.month, year=date.year).strftime('%Y/%m/%d')
        return date_type

    
    def delete_patient(self):
        
        self.messagebox = QMessageBox()
        self.messagebox.setIcon(QMessageBox.Question)
        self.messagebox.setWindowIcon(QtGui.QIcon(':/images/TebNoLogo.png'))
        self.messagebox.setWindowTitle("حذف بیمار")
        self.messagebox.setFont(self.font)
        self.messagebox.setText("آیا از حذف بیمار مورد نظر مطمئن هستید؟")
        self.messagebox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.messagebox.button(QMessageBox.Yes).setText('بلی')
        self.messagebox.button(QMessageBox.No).setText('خیر')
        result = self.messagebox.exec_()

        if(result == QMessageBox.Yes):
            message = PatientOperations.deletePatient(self.patient_ncode)
            if(message == "بیمار مورد نظر حذف شد."):
                self.patientsList.setModel(PatientModel(self, ['نام','نام خانوادگی', 'کد ملی', 'شماره همراه']))
                self.visitsMain.setModel(AllVisitsModel(self, ['نام خانوادگی', 'کد ملی','تاریخ', 'ساعت', 'وضعیت']))
            self.close()
        
        
    
    def addVisit(self):

        args = {
            'ncode': self.patient_ncode,
            'hour': unidecode(self.visitTime.text()),
            'date': unidecode(self.visitDate.text())
        }
        message = VisitOperations.addVisit(**args)
        self.clear_save_visit_btn()
        self.setVisitsListInfo()
        self.messagebox = TimerMessageBox(3, message, self.font)
        self.messagebox.exec_()
    
    def clear_save_visit_btn(self):
        self.visitTime.setText('')
        self.visitDate.setText('')

    def setVisitsListInfo(self):
        self.visitsList.setModel(VisitModel(self, ['شناسه', 'تاریخ', 'ساعت', 'وضعیت'], self.patient_ncode))
        self.visitsMain.setModel(AllVisitsModel(self, ['نام خانوادگی', 'کد ملی','تاریخ', 'ساعت', 'وضعیت']))
        self.patientsList.setModel(PatientModel(self, ['نام','نام خانوادگی', 'کد ملی', 'شماره همراه']))
    
    def visitsShow(self):
        indexes = self.visitsList.selectionModel().selectedIndexes()
        for index in indexes:
            id = index.child(index.row(), 0).data()
            status = index.child(index.row(), 3).data()
        
        if(status == "نامشخص" or status=="تایید شده"):
            
            self.visitDialog.visit_id = int(id)
            self.visitDialog.setScreen()
            self.visitDialog.visitsList = self.visitsList
            self.visitDialog.visitsMain = self.visitsMain
            self.visitDialog.closed.connect(self.show)
            self.hide()
            self.visitDialog.show()
        
        # QMessageBox.information(self, 'Information', message)

    
    def createFile(self):
        result=CreateReport.create_file(self.patient_ncode)
        file_name, _ = QFileDialog.getSaveFileName(self, "ذخیره اطلاعات بیمار", "", "Html Files (*.html)")
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(result)
            self.messagebox = TimerMessageBox(3, 'فایل ذخیره شد.', self.font)
            self.messagebox.exec_()
            
    def eventFilter(self, source, event):
        
        if event.type() == QtCore.QEvent.MouseButtonPress:

            if source == self.visitTime:
                self.visitTime.setFocus(QtCore.Qt.MouseFocusReason)
                self.visitTime.setCursorPosition(0)
                return True
            
            if source == self.visitDate:
                self.visitDate.setFocus(QtCore.Qt.MouseFocusReason)
                self.visitDate.setCursorPosition(1)
                return True

        return super().eventFilter(source, event)
    

    




# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PatientScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
from VisitModel import VisitModel
import resources
import os
from OSHandling import OSHandling

class Ui_patientInfo(object):
    def setupUi(self, patientInfo):
        QtGui.QFontDatabase.addApplicationFont(':/fonts/Vazirmatn-Bold.ttf')
        self.font = QtGui.QFont()
        self.font.setFamily("Vazirmatn")
        self.font.setPointSize(10)
        patientInfo.setObjectName("patientInfo")
        patientInfo.resize(700, 650)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(patientInfo.sizePolicy().hasHeightForWidth())
        patientInfo.setSizePolicy(sizePolicy)
        patientInfo.setMinimumSize(QtCore.QSize(700, 650))
        patientInfo.setMaximumSize(QtCore.QSize(700, 650))
        #Style Path
        with open(OSHandling.styleHandling(), 'r') as f:
            patientInfo.setStyleSheet(f.read())
        self.patientTab = QtWidgets.QTabWidget(patientInfo)
        self.patientTab.setGeometry(QtCore.QRect(100, 0, 600, 600))
        self.patientTab.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.patientTab.setObjectName("patientTab")
        self.patientInformation = QtWidgets.QWidget()
        self.patientInformation.setObjectName("patientInformation")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.patientInformation)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name_lbl = QtWidgets.QLabel(self.patientInformation)
        self.name_lbl.setObjectName("name_lbl")
        self.verticalLayout.addWidget(self.name_lbl)
        self.name = QtWidgets.QLineEdit(self.patientInformation)
        self.name.setMaxLength(30)
        self.name.setObjectName("name")
        self.name.setFont(self.font)
        self.verticalLayout.addWidget(self.name)
        self.fname_lbl = QtWidgets.QLabel(self.patientInformation)
        self.fname_lbl.setObjectName("fname_lbl")
        self.verticalLayout.addWidget(self.fname_lbl)
        self.fname = QtWidgets.QLineEdit(self.patientInformation)
        self.fname.setMaxLength(35)
        self.fname.setObjectName("fname")
        self.fname.setFont(self.font)
        self.verticalLayout.addWidget(self.fname)
        self.phone_lbl = QtWidgets.QLabel(self.patientInformation)
        self.phone_lbl.setObjectName("phone_lbl")
        self.verticalLayout.addWidget(self.phone_lbl)
        self.phoneNumber = QtWidgets.QLineEdit(self.patientInformation)
        self.phoneNumber.setObjectName("phoneNumber")
        self.verticalLayout.addWidget(self.phoneNumber)
        self.ncode_lbl = QtWidgets.QLabel(self.patientInformation)
        self.ncode_lbl.setObjectName("ncode_lbl")
        self.verticalLayout.addWidget(self.ncode_lbl)
        self.nationalCode = QtWidgets.QLineEdit(self.patientInformation)
        self.nationalCode.setObjectName("nationalCode")
        self.verticalLayout.addWidget(self.nationalCode)
        self.date_lbl = QtWidgets.QLabel(self.patientInformation)
        self.date_lbl.setObjectName("date_lbl")
        self.verticalLayout.addWidget(self.date_lbl)
        self.birth = QtWidgets.QLineEdit(self.patientInformation)
        self.birth.setObjectName("birth")
        self.verticalLayout.addWidget(self.birth)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.editPatient = QtWidgets.QPushButton(self.patientInformation)
        self.editPatient.setObjectName("editPatient")
        self.horizontalLayout.addWidget(self.editPatient)
        self.deletePatient = QtWidgets.QPushButton(self.patientInformation)
        self.deletePatient.setObjectName("deletePatient")
        self.horizontalLayout.addWidget(self.deletePatient)
        self.verticalLayout.addLayout(self.horizontalLayout)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/person.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.patientTab.addTab(self.patientInformation, icon, "")
        
        self.visitsTab = QtWidgets.QWidget()
        self.visitsTab.setObjectName("visitsTab")
        # self.visit_lbl = QtWidgets.QLabel(self.visitsTab)
        # self.visit_lbl.setGeometry(QtCore.QRect(200, 80, 61, 31))
        # self.visit_lbl.setObjectName("visit_lbl")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.visitsTab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 40, 501, 451))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.visitScreen = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.visitScreen.setContentsMargins(0, 0, 0, 0)
        self.visitScreen.setObjectName("visitScreen")
        self.visitsList = QtWidgets.QTableView()
        self.visitsList.setFont(self.font)
        self.visit_model = VisitModel(self, ['شناسه', 'تاریخ', 'ساعت', 'وضعیت'])
        self.visitsList.setModel(self.visit_model)
        self.visitScreen.addWidget(self.visitsList)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/visits.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.patientTab.addTab(self.visitsTab, icon1, "")
        
        self.newVisit = QtWidgets.QWidget()
        self.newVisit.setObjectName("newVisit")
        self.formLayout_2 = QtWidgets.QFormLayout(self.newVisit)
        self.formLayout_2.setObjectName("formLayout_2")
        self.time = QtWidgets.QLabel(self.newVisit)
        self.time.setObjectName("time")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.time)
        self.visit = QtWidgets.QLabel(self.newVisit)
        self.visit.setObjectName("visit")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.visit)
        self.visitDate = QtWidgets.QLineEdit(self.newVisit)
        self.visitDate.setObjectName("visitDate")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.visitDate)
        self.visitTime = QtWidgets.QLineEdit(self.newVisit)
        self.visitTime.setAlignment(QtCore.Qt.AlignCenter)
        self.visitTime.setObjectName("visitTime")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.visitTime)
        self.visitBtn = QtWidgets.QPushButton(self.newVisit)
        self.visitBtn.setObjectName("visitBtn")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.visitBtn)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(8, QtWidgets.QFormLayout.FieldRole, spacerItem)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/createVisit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.patientTab.addTab(self.newVisit, icon2, "")

        #Print Patient Info
        self.patientInfoFile = QtWidgets.QWidget()
        self.InfoLayout = QtWidgets.QVBoxLayout(self.patientInfoFile)
        self.patientInfoBtn = QtWidgets.QPushButton(self.patientInfoFile)
        self.patientInfoBtn.setObjectName("patientInfoBtn")
        self.InfoLayout.addWidget(self.patientInfoBtn)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.patientTab.addTab(self.patientInfoFile, icon1, "")

        self.retranslateUi(patientInfo)
        self.patientTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(patientInfo)

    def retranslateUi(self, patientInfo):
        _translate = QtCore.QCoreApplication.translate
        patientInfo.setWindowTitle(_translate("patientInfo", "Form"))
        self.name_lbl.setText(_translate("patientInfo", "نام:"))
        self.fname_lbl.setText(_translate("patientInfo", "نام خانوادگی:"))
        self.phone_lbl.setText(_translate("patientInfo", "شماره همراه:"))
        self.phoneNumber.setInputMask(_translate("patientInfo", "99999999999"))
        self.ncode_lbl.setText(_translate("patientInfo", "کد ملی:"))
        self.nationalCode.setInputMask(_translate("patientInfo", "9999999999"))
        self.date_lbl.setText(_translate("patientInfo", "تاریخ تولد:"))
        self.birth.setInputMask(_translate("patientInfo", "1999/99/99"))
        self.editPatient.setText(_translate("patientInfo", "ویرایش"))
        self.deletePatient.setText(_translate("patientInfo", "حذف"))
        self.patientTab.setTabText(self.patientTab.indexOf(self.patientInformation), _translate("patientInfo", "اطلاعات پایه"))
        # self.visit_lbl.setText(_translate("patientInfo", "نوبت‌ها:"))
        self.patientTab.setTabText(self.patientTab.indexOf(self.visitsTab), _translate("patientInfo", "نوبت‌ها"))

        self.time.setText(_translate("TebNoContainer", "ساعت نوبت:"))
        self.visit.setText(_translate("TebNoContainer", "تاریخ نوبت:"))
        self.visitDate.setInputMask(_translate("TebNoContainer", "1999/99/99"))
        self.visitTime.setInputMask(_translate("TebNoContainer", "99:99"))
        self.visitBtn.setText(_translate("TebNoContainer", "ثبت نوبت"))
        self.patientInfoBtn.setText(_translate("TebNoContainer", "ایجاد فایل اطلاعات بیمار"))
        self.patientTab.setTabText(self.patientTab.indexOf(self.newVisit), _translate("TebNoContainer", "ایجاد نوبت"))
        self.patientTab.setTabText(self.patientTab.indexOf(self.patientInfoFile), _translate("TebNoContainer", "فایل اطلاعات فرد"))





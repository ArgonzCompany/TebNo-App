from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
import datetime
from database import VisitOperations, PatientOperations
from PyQt5 import QtCore

class VisitModel(QtCore.QAbstractTableModel):

    def __init__(self, parent, header, patient_ncode=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        if(patient_ncode == 0 or  patient_ncode is None):
            results = list([])
        else:
            results = VisitOperations.show_visits(patient_ncode)
        self.mylist = results
        self.header = header

    def rowCount(self, parent):
        if len(self.mylist) == 0:
            return 0
        return len(self.mylist)

    def columnCount(self, parent):
        if len(self.mylist) == 0:
            return 0
        return len(self.mylist[0])

    def data(self, index, role):
        # 5. populate data
        if not index.isValid():
            return None
        

        if (role == Qt.DisplayRole):
            value = self.mylist[index.row()][index.column()]
            
            if isinstance(value, datetime.date):
                date = PatientOperations.convert_to_jalali(value).strftime('%Y/%m/%d') 
                return date       

            if isinstance(value, int):
                if index.column() == 3:
                    if value == 1:
                        return f"نامشخص"
                    if value == 2:
                        return f"تایید شده"
                    if value == 3:
                        return f"لغو شده"
           
            return value
        

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
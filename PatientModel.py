
from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
from database import PatientOperations
from PyQt5 import QtCore

class PatientModel(QtCore.QAbstractTableModel):

    def __init__(self, parent, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        results = PatientOperations.show_patients()
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
            return self.mylist[index.row()][index.column()]
        else:
            return QVariant()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
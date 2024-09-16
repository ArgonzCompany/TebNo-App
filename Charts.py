from database import Patient, PatientOperations, VisitOperations
import resources
from TimerBox import TimerMessageBox
import datetime as dt
from pathlib import Path
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import (QBarCategoryAxis, QBarSeries, QBarSet, QChart,
                              QChartView, QLineSeries, QValueAxis, QHorizontalStackedBarSeries)
import pyqtgraph as pg


class VisitsChart(QMainWindow):
    closed = QtCore.pyqtSignal()
    def __init__(self, visits):
        super().__init__()
        QtGui.QFontDatabase.addApplicationFont(':/fonts/Vazirmatn-Bold.ttf')
        self.font = QtGui.QFont()
        self.font.setFamily("Vazirmatn")
        self.font.setPointSize(12)
        self.visits = visits     
        self.setMinimumSize(QSize(400,400))
        self.setWindowTitle("وضعیت نوبت‌ها")
        self.setWindowIcon(QtGui.QIcon(':/images/TebNoLogo.png'))
        
        self.visits = {k: self.visits[k] for k in list(self.visits.keys())[:4]}

        list_undefined = []
        list_verified = []
        list_canceled = []

        self.set0 = QBarSet("نامشخص")
        self.set0.setColor(QColor("#335ECC"))
        self.set1 = QBarSet("تایید شده")
        self.set1.setColor(QColor("#33CC54"))
        self.set2 = QBarSet("لغو شده")
        self.set2.setColor(QColor("#CC33AB"))


        for key in self.visits.keys():
            self.set0.append(self.visits[key]["نامشخص"])
            list_undefined.append(self.visits[key]["نامشخص"])
            self.set1.append(self.visits[key]["تایید شده"])
            list_verified.append(self.visits[key]["تایید شده"])
            self.set2.append(self.visits[key]["لغو شده"])
            list_canceled.append(self.visits[key]["لغو شده"])
        

        self._bar_series = QBarSeries()
        self._bar_series.append(self.set0)
        self._bar_series.append(self.set1)
        self._bar_series.append(self.set2)

    

        self.chart = QChart()
        self.chart.addSeries(self._bar_series)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chart.setTitle("نوبت‌ها در ماه‌های مختلف")
        self.chart.setTitleFont(self.font)
        self.chart.setTitleBrush(QColor("#645531"))

        self.categories = list(self.visits.keys())
        self._axis_x = QBarCategoryAxis()
        self._axis_x.append(self.categories)
        self.label_font = QtGui.QFont('Times New Roman', 12)
        self.label_font.setBold(True)
        self._axis_x.setLabelsFont(self.label_font)
        self._axis_x.setLabelsBrush(QBrush(QColor("#645531")))
        self.chart.addAxis(self._axis_x, Qt.AlignBottom)
        self._bar_series.attachAxis(self._axis_x)
        self._axis_x.setRange(self.categories[0], self.categories[len(self.categories)-1])

        self._axis_y = QValueAxis()
        self._axis_y.setLabelsFont(self.label_font)
        self._axis_y.setLabelsBrush(QBrush(QColor("#645531")))
        self.chart.addAxis(self._axis_y, Qt.AlignLeft)
        self._bar_series.attachAxis(self._axis_y)
        self._axis_y.setRange(0, max(max(list_undefined), max(list_verified), max(list_canceled)))

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.legend().setFont(self.font)
        self.chart.legend().setLabelColor(QColor("#645531"))

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)
        self._chart_view.chart().setBackgroundBrush(QBrush(QColor("#cca133")))


        self.setCentralWidget(self._chart_view)
    
    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)






class PatientsChart(QMainWindow):
    closed = QtCore.pyqtSignal()
    def __init__(self, ages):
        super().__init__()
        QtGui.QFontDatabase.addApplicationFont(':/fonts/Vazirmatn-Bold.ttf')
        self.font = QtGui.QFont()
        self.font.setFamily("Vazirmatn")
        self.font.setPointSize(12)
        self.ages = ages
        
        

        self.setMinimumSize(QSize(400,400))
        self.setWindowTitle("بازه سنی بیماران")
        self.setWindowIcon(QtGui.QIcon(':/images/TebNoLogo.png'))

        
        ages_set = dict()
        for age in sorted(set(self.ages)):
            ages_set[str(age)] = self.ages.count(age)
        
        
        self._bar_series = QBarSeries()
        for key in ages_set.keys():
            barset = QBarSet(key)
            barset.append(ages_set.get(key))
            self._bar_series.append(barset)
        
        

        self.chart = QChart()
        self.chart.addSeries(self._bar_series)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chart.setTitle("وضعیت بیماران")
        self.chart.setTitleFont(self.font)
        self.chart.setTitleBrush(QColor("#645531"))

        self._axis_x = QBarCategoryAxis()
        self._axis_x.append("بازه سنی")
        self.label_font = QtGui.QFont('Times New Roman', 12)
        self.label_font.setBold(True)
        self._axis_x.setLabelsFont(self.font)
        self._axis_x.setLabelsBrush(QBrush(QColor("#645531")))
        self.chart.addAxis(self._axis_x, Qt.AlignBottom)
        self._bar_series.attachAxis(self._axis_x)
        self._axis_x.setRange(min(ages_set.keys()), max(ages_set.keys()))

        self._axis_y = QValueAxis()
        self._axis_y.setLabelsFont(self.label_font)
        self._axis_y.setLabelsBrush(QBrush(QColor("#645531")))
        self.chart.addAxis(self._axis_y, Qt.AlignLeft)
        self._bar_series.attachAxis(self._axis_y)
        self._axis_y.setRange(0, max(ages_set.values()))

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.legend().setFont(self.font)
        self.chart.legend().setLabelColor(QColor("#645531"))

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)
        self._chart_view.chart().setBackgroundBrush(QBrush(QColor("#cca133")))


        self.setCentralWidget(self._chart_view)
    
    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)



# class VisitPriority(QMainWindow):
#     closed = QtCore.pyqtSignal()
#     def __init__(self, results):
#         super().__init__()
#         QtGui.QFontDatabase.addApplicationFont(':/fonts/Vazirmatn-Bold.ttf')
#         self.font = QtGui.QFont()
#         self.font.setFamily("Vazirmatn")
#         self.font.setPointSize(12)
#         self.results = results
        
        

#         self.setMinimumSize(QSize(400,400))
#         self.setWindowTitle("نمودار نوبت‌ها")
#         self.setWindowIcon(QtGui.QIcon(':/images/TebNoLogo.png'))

        
        
        
#         self._bar_series = QHorizontalStackedBarSeries()
#         barset = dict()
#         for key in self.results.keys():
#             if not barset.get(key):
#                 barset[key] = QBarSet(key)
        
#         for key in self.results.keys():
#             for key1 in self.results[key].keys():
#                 barset1 = QBarSet(key1)
#                 barset1.append(self.results[key][key1])
#                 barset[key].append(barset1)
        
#         for key in barset.keys():
#              self._bar_series.append(barset[key])
        

#         self.chart = QChart()
#         self.chart.addSeries(self._bar_series)
#         self.chart.setAnimationOptions(QChart.SeriesAnimations)

#         self.chart.setTitle("زمان نوبت‌ها")
#         self.chart.setTitleFont(self.font)
#         self.chart.setTitleBrush(QColor("#645531"))

#         self._axis_y = QBarCategoryAxis()
#         self._axis_y.append(self.results.keys())
#         self.label_font = QtGui.QFont('Times New Roman', 12)
#         self.label_font.setBold(True)
#         self._axis_y.setLabelsFont(self.font)
#         self._axis_y.setLabelsBrush(QBrush(QColor("#645531")))
#         self.chart.addAxis(self._axis_y, Qt.AlignLeft)
#         self._bar_series.attachAxis(self._axis_y)
#         # self._axis_x.setRange(min(ages_set.keys()), max(ages_set.keys()))

#         self._axis_x = QValueAxis()
#         self._axis_x.setLabelsFont(self.label_font)
#         self._axis_x.setLabelsBrush(QBrush(QColor("#645531")))
#         self.chart.addAxis(self._axis_x, Qt.AlignBottom)
#         self._bar_series.attachAxis(self._axis_x)
#         # self._axis_y.setRange(0, max(ages_set.values()))

#         self.chart.legend().setVisible(True)
#         self.chart.legend().setAlignment(Qt.AlignBottom)
#         self.chart.legend().setFont(self.font)
#         self.chart.legend().setLabelColor(QColor("#645531"))

#         self._chart_view = QChartView(self.chart)
#         self._chart_view.setRenderHint(QPainter.Antialiasing)
#         self._chart_view.chart().setBackgroundBrush(QBrush(QColor("#cca133")))


#         self.setCentralWidget(self._chart_view)
    
#     def closeEvent(self, event):
#         self.closed.emit()
#         super().closeEvent(event)



class VisitPriority(QMainWindow):
    closed = QtCore.pyqtSignal()
    def __init__(self, results):
        super().__init__()
        self.results = results
        self.setWindowTitle("نوبت‌ها در روزهای آتی")
        self.setGeometry(100, 100, 700, 600)
        self.setWindowIcon(QtGui.QIcon(':/images/TebNoLogo.png'))
        self.UiComponents()

    def UiComponents(self):
 
        widget = QWidget()

        x_data = list()
 
        y_data = list()

        y_labels = list()
        x_labels = list()

        for key1 in self.results.keys():
            temp = key1.split('-')
            y_labels.append((int(temp[2]), key1))
            for key2 in self.results[key1].keys():
                x_data.append(self.results[key1][key2])
                x_labels.append((self.results[key1][key2], "ساعت"+key2))
                y_data.append(int(temp[2]))
 
        plot = pg.plot()
        pen1 = pg.mkPen(color = '#645531', width=3)
        pen2 = pg.mkPen(color = '#01131d', width=10)
        x_labels = list(set(x_labels))
 
        scatter = pg.ScatterPlotItem(
            size=20, brush=pg.mkBrush('#0E9FF1'))
 
 
        scatter.addPoints(x_data, y_data)
 
        plot.addItem(scatter)
        plot.setBackground('#F9B006')
        plot.plotItem.getAxis('left').setPen(pen1)
        plot.plotItem.getAxis('left').setTextPen(pen2)
        plot.plotItem.getAxis('left').setTicks([y_labels])
        plot.plotItem.getAxis('bottom').setPen(pen1)
        plot.plotItem.getAxis('bottom').setTextPen(pen2)
        plot.plotItem.getAxis('bottom').setTicks([x_labels])
        plot.setYRange(1, 31)
 
        layout = QGridLayout()
 
        widget.setLayout(layout)
 
        layout.addWidget(plot, 0, 1, 3, 1)


 
        self.setCentralWidget(widget)
    
    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
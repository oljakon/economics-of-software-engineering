import sys
from matplotlib import pyplot as plt
import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QComboBox, QHeaderView, QTableWidgetItem


parameters = {
    'RELY': [0.75, 0.86, 1.0, 1.15, 1.40],
    'DATA': [0.94, 1.0, 1.08, 1.16],
    'CPLX': [0.70, 0.85, 1.0, 1.15, 1.30],
    'TIME': [1.0, 1.11, 1.50],
    'STOR': [1.0, 1.06, 1.21],
    'VIRT': [0.87, 1.0, 1.15, 1.30],
    'TURN': [0.87, 1.0, 1.07, 1.15],
    'ACAP': [1.46, 1.19, 1.0, 0.86, 0.71],
    'AEXP': [1.29, 1.15, 1.0, 0.91, 0.82],
    'PCAP': [1.42, 1.17, 1.0, 0.86, 0.70],
    'VEXP': [1.21, 1.10, 1.0, 0.90],
    'LEXP': [1.14, 1.07, 1.0, 0.95],
    'MODP': [1.24, 1.10, 1.0, 0.91, 0.82],
    'TOOL': [1.24, 1.10, 1.0, 0.91, 0.82],
    'SCED': [1.23, 1.08, 1.0, 1.04, 1.10],
}

project_modes = {
    'c1': [3.2, 3.0, 2.8],
    'p1': [1.05, 1.12, 1.2],
    'c2': [2.5, 2.5, 2.5],
    'p2': [0.38, 0.35, 0.32]
}


def PM(c1, p1, EAF, SIZE):
    return c1 * EAF * (SIZE ** p1)


def TM(c2, p2, PM):
    return c2 * (PM ** p2)


def calc_EAF(params: list):
    return np.prod(params)


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = uic.loadUi('window.ui', self)

        self.RELY: QComboBox = self.ui.comboBox_1
        self.DATA: QComboBox = self.ui.comboBox_2
        self.CPLX: QComboBox = self.ui.comboBox_3
        self.TIME: QComboBox = self.ui.comboBox_4
        self.STOR: QComboBox = self.ui.comboBox_5
        self.VIRT: QComboBox = self.ui.comboBox_6
        self.TURN: QComboBox = self.ui.comboBox_7
        self.ACAP: QComboBox = self.ui.comboBox_8
        self.AEXP: QComboBox = self.ui.comboBox_9
        self.PCAP: QComboBox = self.ui.comboBox_10
        self.VEXP: QComboBox = self.ui.comboBox_11
        self.LEXP: QComboBox = self.ui.comboBox_12
        self.MODP: QComboBox = self.ui.comboBox_13
        self.TOOL: QComboBox = self.ui.comboBox_14
        self.SCED: QComboBox = self.ui.comboBox_15

        self.SIZE: QLineEdit = self.ui.sizeEdit

        self.COST: QLineEdit = self.ui.costEdit

        self.project_mode: QComboBox = self.ui.comboBox_16

        self.ui.wbsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.classicTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def EAF(self):
        RELY = parameters['RELY'][self.RELY.currentIndex()]
        DATA = parameters['DATA'][self.DATA.currentIndex()]
        CPLX = parameters['CPLX'][self.CPLX.currentIndex()]
        TIME = parameters['TIME'][self.TIME.currentIndex()]
        STOR = parameters['STOR'][self.STOR.currentIndex()]
        VIRT = parameters['VIRT'][self.VIRT.currentIndex()]
        TURN = parameters['TURN'][self.TURN.currentIndex()]
        ACAP = parameters['ACAP'][self.ACAP.currentIndex()]
        AEXP = parameters['AEXP'][self.AEXP.currentIndex()]
        PCAP = parameters['PCAP'][self.PCAP.currentIndex()]
        VEXP = parameters['VEXP'][self.VEXP.currentIndex()]
        LEXP = parameters['LEXP'][self.LEXP.currentIndex()]
        MODP = parameters['MODP'][self.MODP.currentIndex()]
        TOOL = parameters['TOOL'][self.TOOL.currentIndex()]
        SCED = parameters['SCED'][self.SCED.currentIndex()]

        return RELY * DATA * CPLX * TIME * STOR * VIRT * TURN * ACAP * AEXP * PCAP * VEXP * LEXP * MODP * TOOL * SCED

    def PM(self):
        mode = self.project_mode.currentIndex()
        size = float(self.SIZE.text())

        return project_modes['c1'][mode] * self.EAF() * (size ** project_modes['p1'][mode])

    def TM(self):
        mode = self.project_mode.currentIndex()

        return project_modes['c2'][mode] * (self.PM() ** project_modes['p2'][mode])

    @pyqtSlot(name="on_calculateButton_clicked")
    def calculate_project(self):
        pm_clean = round(self.PM(), 2)
        tm_clean = round(self.TM(), 2)
        pm = round(pm_clean * 1.08, 2)
        tm = round(tm_clean * 1.36, 2)

        self.ui.pmLabel.setText(f'Трудоемкость: {pm}')
        self.ui.tmLabel.setText(f'Время разработки: {tm}')

        for i in range(8):
            self.ui.wbsTable.setItem(i, 1, QTableWidgetItem(
                str(round(pm * int(self.ui.wbsTable.item(i, 0).text()) / 100.0, 2))))
        self.ui.wbsTable.setItem(8, 1, QTableWidgetItem(str(pm)))

        self.ui.classicTable.setItem(0, 0, QTableWidgetItem(str(round(pm_clean * 0.08, 2))))
        self.ui.classicTable.setItem(1, 0, QTableWidgetItem(str(round(pm_clean * 0.18, 2))))
        self.ui.classicTable.setItem(2, 0, QTableWidgetItem(str(round(pm_clean * 0.25, 2))))
        self.ui.classicTable.setItem(3, 0, QTableWidgetItem(str(round(pm_clean * 0.26, 2))))
        self.ui.classicTable.setItem(4, 0, QTableWidgetItem(str(round(pm_clean * 0.31, 2))))
        self.ui.classicTable.setItem(5, 0, QTableWidgetItem(str(round(pm_clean, 2))))
        self.ui.classicTable.setItem(6, 0, QTableWidgetItem(str(round(pm, 2))))
        self.ui.classicTable.setItem(0, 1, QTableWidgetItem(str(round(tm_clean * 0.36, 2))))
        self.ui.classicTable.setItem(1, 1, QTableWidgetItem(str(round(tm_clean * 0.36, 2))))
        self.ui.classicTable.setItem(2, 1, QTableWidgetItem(str(round(tm_clean * 0.18, 2))))
        self.ui.classicTable.setItem(3, 1, QTableWidgetItem(str(round(tm_clean * 0.18, 2))))
        self.ui.classicTable.setItem(4, 1, QTableWidgetItem(str(round(tm_clean * 0.28, 2))))
        self.ui.classicTable.setItem(5, 1, QTableWidgetItem(str(round(tm_clean, 2))))
        self.ui.classicTable.setItem(6, 1, QTableWidgetItem(str(round(tm, 2))))

        y = []
        for i in range(5):
            t = round(float(self.ui.classicTable.item(i, 1).text()))
            for j in range(t):
                y.append(round(round(float(self.ui.classicTable.item(i, 0).text())) / t))

        x = [i + 1 for i in range(len(y))]

        workers_sum = 0

        plt.bar(x, y)
        for xi in x:
            plt.annotate(str(y[xi - 1]), (xi, y[xi - 1]), ha='center')
            workers_sum += y[xi - 1]
        plt.show()
        workers_avg = workers_sum // len(x)

        budget = round(float(self.COST.text()) * tm * workers_avg, 2)
        self.ui.costLabel.setText(f'Приблизительный бюджет: {budget}')

    @pyqtSlot(name="on_graphsButton_clicked")
    def create_graphs(self):
        for sced in [0, 2, 4]:
            for t in range(3):
                y_modp_pm = []
                y_tool_pm = []
                y_modp_tm = []
                y_tool_tm = []

                x = [1, 2, 3, 4, 5]

                for i in range(5):
                    y_modp_pm.append(PM(project_modes['c1'][t], project_modes['p1'][t], calc_EAF([
                        parameters['MODP'][i], parameters['SCED'][sced]]), 100))
                    y_modp_tm.append(TM(project_modes['c2'][t], project_modes['p2'][t], y_modp_pm[-1]))

                    y_tool_pm.append(PM(project_modes['c1'][t], project_modes['p1'][t], calc_EAF([
                        parameters['TOOL'][i], parameters['SCED'][sced]]), 100))
                    y_tool_tm.append(TM(project_modes['c2'][t], project_modes['p2'][t], y_tool_pm[-1]))

                plt.suptitle(f'PM, TM')
                plt.subplot(121)
                line1, = plt.plot(x, y_modp_pm, 'r', label='MODP')
                line2, = plt.plot(x, y_tool_pm, 'g', label='TOOL')
                plt.subplot(122)
                plt.plot(x, y_modp_tm, 'r', x, y_tool_tm, 'g')
                plt.legend(handles=[line1, line2])
                plt.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
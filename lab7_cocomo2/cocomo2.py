from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
from math import ceil

power_params_table = {
    'PREC': [6.2, 4.96, 3.72, 2.48, 1.24, 0.0],
    'FLEX': [5.07, 4.05, 3.04, 2.03, 1.01, 0.0],
    'RESL': [7.07, 5.65, 4.24, 2.83, 1.41, 0.0],
    'TEAM': [5.48, 4.38, 3.29, 2.19, 1.10, 0.0],
    'PMAT': [7.8, 6.24, 4.68, 3.12, 1.56, 0.0]
}

labor_factor_table = {
    'PERS': [1.62, 1.26, 1.00, 0.83, 0.63, 0.50],
    'RCPX': [0.60, 0.83, 1.00, 1.33, 1.91, 2.72],
    'RUSE': [0.95, 1.00, 1.07, 1.15, 1.24],
    'PDIF': [0.87, 1.00, 1.29, 1.81, 2.61],
    'PREX': [1.33, 1.22, 1.00, 0.87, 0.74, 0.62],
    'FCIL': [1.30, 1.10, 1.00, 0.87, 0.73, 0.62],
    'SCED': [1.43, 1.14, 1.00, 1.00, 1.00]
}


class MyWindow(QMainWindow):
    def __init__(self, loc):
        QWidget.__init__(self)

        uic.loadUi("cocomo2.ui", self)

        self.pushButtonCalculate.clicked.connect(lambda: button_calculate_1())
        self.pushButtonCalculate_2.clicked.connect(lambda: button_calculate_2())

        self.PREC: QComboBox = self.findChild(QComboBox, 'powComboBox_1')
        self.FLEX: QComboBox = self.findChild(QComboBox, 'powComboBox_2')
        self.RESL: QComboBox = self.findChild(QComboBox, 'powComboBox_3')
        self.TEAM: QComboBox = self.findChild(QComboBox, 'powComboBox_4')
        self.PMAT: QComboBox = self.findChild(QComboBox, 'powComboBox_5')

        self.PERS: QComboBox = self.findChild(QComboBox, 'archComboBox_1')
        self.RCPX: QComboBox = self.findChild(QComboBox, 'archComboBox_2')
        self.RUSE: QComboBox = self.findChild(QComboBox, 'archComboBox_3')
        self.PDIF: QComboBox = self.findChild(QComboBox, 'archComboBox_4')
        self.PREX: QComboBox = self.findChild(QComboBox, 'archComboBox_5')
        self.FCIL: QComboBox = self.findChild(QComboBox, 'archComboBox_6')
        self.SCED: QComboBox = self.findChild(QComboBox, 'archComboBox_7')

        self.lineEditLines.setText(str(loc))

        def button_calculate_1():
            work, time = calculate_cocomo2_model_1(calculate_earch(), calculate_object_points(), calculate_power())

            self.label_work.setText(str(round(work, 3)))
            self.label_time.setText(str(round(time, 3)))
            self.label_workers.setText(str(ceil(work / time)))
            self.label_budget.setText(str(round(work * float(self.lineEditSalary.text()), 3)))

        def button_calculate_2():
            lines = int(self.lineEditLines.text()) / 1000
            work, time = calculate_cocomo2_model_2(calculate_earch(), lines, calculate_power())

            self.label_work_2.setText(str(round(work, 3)))
            self.label_time_2.setText(str(round(time, 3)))
            self.label_workers_2.setText(str(ceil(work / time)))
            self.label_budget_2.setText(str(round(work * float(self.lineEditSalary_2.text()), 3)))

        def calculate_cocomo2_model_1(earch, object_points, power):
            prod_table = [4, 7, 13, 25, 50]
            nop = object_points * (100 - float(self.lineEditRUSE.text())) / 100
            work = nop / prod_table[self.comboBoxXP.currentIndex()]
            time = 3 * work ** (0.33 + 0.2 * (power - 1.01))

            return work, time

        def calculate_cocomo2_model_2(earch, ksloc, power):
            work = 2.45 * earch * ksloc ** power
            time = 3 * work ** (0.33 + 0.2 * (power - 1.01))

            return work, time

        def calculate_object_points():
            forms = int(self.lineEditForms_0.text()) + int(self.lineEditForms_1.text()) * 2 + \
                    int(self.lineEditForms_2.text()) * 3
            reports = int(self.lineEditReport_0.text()) * 2 + int(self.lineEditReport_1.text()) * 5 + \
                      int(self.lineEditReport_2.text()) * 8
            third_gen_language = int(self.lineEditLanguages.text()) * 10
            return forms + reports + third_gen_language

        def calculate_power():
            power_params = self.get_power_params()

            PREC = power_params_table['PREC'][power_params['PREC']]
            FLEX = power_params_table['FLEX'][power_params['FLEX']]
            RESL = power_params_table['RESL'][power_params['RESL']]
            TEAM = power_params_table['TEAM'][power_params['TEAM']]
            PMAT = power_params_table['PMAT'][power_params['PMAT']]

            power = 0

            power += PREC
            power += FLEX
            power += RESL
            power += TEAM
            power += PMAT

            power = power / 100 + 1.01

            return power

        def calculate_earch():
            earch_params = self.get_earch_params()
            result = 1

            result *= labor_factor_table['PERS'][earch_params['PERS']]
            result *= labor_factor_table['RCPX'][earch_params['RCPX']]
            result *= labor_factor_table['RUSE'][earch_params['RUSE']]
            result *= labor_factor_table['PDIF'][earch_params['PDIF']]
            result *= labor_factor_table['PREX'][earch_params['PREX']]
            result *= labor_factor_table['FCIL'][earch_params['FCIL']]
            result *= labor_factor_table['SCED'][earch_params['SCED']]

            return result

    def get_power_params(self):
        return {
            'PREC': self.PREC.currentIndex(),
            'FLEX': self.FLEX.currentIndex(),
            'RESL': self.RESL.currentIndex(),
            'TEAM': self.TEAM.currentIndex(),
            'PMAT': self.PMAT.currentIndex(),
        }

    def get_earch_params(self):
        return {
            'PERS': self.PERS.currentIndex(),
            'RCPX': self.RCPX.currentIndex(),
            'RUSE': self.RUSE.currentIndex(),
            'PDIF': self.PDIF.currentIndex(),
            'PREX': self.PREX.currentIndex(),
            'FCIL': self.FCIL.currentIndex(),
            'SCED': self.SCED.currentIndex(),
        }


if __name__ == '__main__':
    app = QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec())

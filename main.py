import sys
from PyQt5 import uic
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        self.setWindowTitle("Эспрессо!")
        headers = ['ID', 'Название\nсорта', 'Степень\nобжарки\n 1-я, 2-я, 3-я',
                   'Молотый/\nв зернах\n1 - молотый\n2 - в зернах',
                   'Описание вкуса', 'Цена',
                   'Объем упаковки\n(литр)']
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        column_widths = [40, 70, 70, 80, 380, 60, 100]
        for col, width in enumerate(column_widths):
            self.tableWidget.setColumnWidth(col, width)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

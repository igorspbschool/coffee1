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
        headers = ['ID', 'Название\n сорта', 'Степень\n обжарки',
                   'Молотый/\nв зернах\n1 - молотый\n2 - в зернах',
                   'Описание вкуса', 'Цена',
                   'Объем упаковки\n(литр)']
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        column_widths = [40, 70, 70, 80, 380, 60, 100]
        for col, width in enumerate(column_widths):
            self.tableWidget.setColumnWidth(col, width)
        self.pushButton_coffe.clicked.connect(self.adding_change)
        self.statusBar = self.statusBar()
        self.zagruzka_data()

    def zagruzka_data(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()
        cursor.execute(
            "SELECT ID, name_sort, degree_roasting, ground_beans,\
             description_taste, "
            "price, packaging_volume FROM coffee")
        data = cursor.fetchall()
        self.tableWidget.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i, j, item)

        connection.close()

    def adding_change(self):
        self.add_form = AddWidget(self)
        self.add_form.show()


class AddWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle("Эспрессо!")
        self.comboBox.currentIndexChanged.connect(self.load_data)
        self.pushButton_clear.clicked.connect(self.clar_wind)
        self.pushButton_update.clicked.connect(self.update)
        self.pushButton_add.clicked.connect(self.add_sort)
        self.statusBar = self.statusBar()

        self.load_sort()

    def load_sort(self):
        self.comboBox.addItem('Выберите сорт')
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()
        cursor.execute(
            "SELECT ID, name_sort, degree_roasting, ground_beans,\
             description_taste, "
            "price, packaging_volume FROM coffee")
        data = cursor.fetchall()
        self.dict_sort = {}

        for i in data:
            self.dict_sort[i[1]] = (i[0], i[2], i[3], i[4], i[5], i[6])
            self.comboBox.addItem(i[1])
        connection.close()

    def load_data(self):
        if self.comboBox.currentText() != 'Выберите сорт':
            self.description_tastevalue.setText(
                self.dict_sort[self.comboBox.currentText()][3])
            self.name_sortvalue.setText(self.comboBox.currentText())
            self.degree_roastingvalue.setText(
                str(self.dict_sort[self.comboBox.currentText()][1]))
            self.ground_beansvalue.setText(
                str(self.dict_sort[self.comboBox.currentText()][2]))
            self.price_value.setText(str(self.dict_sort[self.comboBox.currentText()][4]))
            self.packaging_volumevalue.setText(
                str(self.dict_sort[self.comboBox.currentText()][5]))

    def clar_wind(self):
        self.description_tastevalue.clear()
        self.name_sortvalue.clear()
        self.degree_roastingvalue.clear()
        self.ground_beansvalue.clear()
        self.price_value.clear()
        self.packaging_volumevalue.clear()
        self.comboBox.setCurrentIndex(0)
        self.pushButton_update.setStyleSheet("background-color: rgb(255, 170, "
                                             "127); color: black")
        self.pushButton_add.setStyleSheet("background-color: rgb(255, 170, "
                                          "127); color: black")

    def update(self):
        try:
            name_sort = self.name_sortvalue.toPlainText()
            degree_roasting = int(self.degree_roastingvalue.toPlainText())
            if degree_roasting not in [1, 2, 3]:
                self.pushButton_update.setStyleSheet(
                    "background-color: red; color: white")
                raise ValueError("Степень обжарки должна быть целым числом от 1 до 3")

            ground_beans = int(self.ground_beansvalue.toPlainText())
            if ground_beans not in [1, 2]:
                self.pushButton_update.setStyleSheet(
                    "background-color: red; color: white")
                raise ValueError("Тип помола должен быть целым числом 1 или 2")
            description_taste = self.description_tastevalue.toPlainText()
            price = self.price_value.toPlainText()
            packaging_volume = self.packaging_volumevalue.toPlainText()

            connection = sqlite3.connect('coffee.sqlite')
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE coffee
                SET name_sort=?, degree_roasting=?,\
                 ground_beans=?, 
                description_taste=?, price=?, packaging_volume=?
                WHERE name_sort=?
            """, (name_sort, degree_roasting, ground_beans, description_taste, price,
                  packaging_volume,
                  self.comboBox.currentText()))
            connection.commit()
            connection.close()
            self.parent().zagruzka_data()
            self.close()
        except Exception as e:
            self.statusbar.showMessage(f"Ошибка обновления данных: {e}")

    def add_sort(self):
        try:
            name_sort = self.name_sortvalue.toPlainText()
            if not name_sort:
                self.statusbar.showMessage("Заполните все поля.")
                self.pushButton_add.setStyleSheet(
                    "background-color: red; color: white")
                return
            degree_roasting = int(self.degree_roastingvalue.toPlainText())
            if not degree_roasting:
                self.statusbar.showMessage("Заполните все поля.")
                self.pushButton_add.setStyleSheet(
                    "background-color: red; color: white")
                return
            if degree_roasting not in [1, 2, 3]:
                self.pushButton_add.setStyleSheet(
                    "background-color: red; color: white")
                raise ValueError("Степень обжарки должна быть целым числом от 1 до 3")

            ground_beans = int(self.ground_beansvalue.toPlainText())
            if not ground_beans:
                self.statusbar.showMessage("Заполните все поля.")
                self.pushButton_add.setStyleSheet(
                    "background-color: red; color: white")
                return
            if ground_beans not in [1, 2]:
                self.pushButton_add.setStyleSheet(
                    "background-color: red; color: white")
                raise ValueError("Тип помола должен быть целым числом 1 или 2")
            description_taste = self.description_tastevalue.toPlainText()
            if not description_taste:
                self.statusbar.showMessage("Заполните все поля.")
                self.pushButton_add.setStyleSheet(
                    "background-color: red; color: white")
                return
            price = self.price_value.toPlainText()
            if not price:
                self.statusbar.showMessage("Заполните все поля.")
                self.pushButton_add.setStyleSheet(
                    "background-color: red; color: white")
                return
            packaging_volume = self.packaging_volumevalue.toPlainText()
            if not packaging_volume:
                self.statusbar.showMessage("Заполните все поля.")
                self.pushButton_add.setStyleSheet(
                    "background-color: red; color: white")
                return

            connection = sqlite3.connect('coffee.sqlite')
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO coffee
                (name_sort, degree_roasting, ground_beans, description_taste, price, 
                packaging_volume) VALUES (?, ?, ?, ?, ?, ?)
            """, (name_sort, degree_roasting, ground_beans, description_taste, price,
                  packaging_volume))
            connection.commit()
            connection.close()
            self.parent().zagruzka_data()
            self.close()
        except Exception as e:
            self.statusbar.showMessage(f"Ошибка обновления данных: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

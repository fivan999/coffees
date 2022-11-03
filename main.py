from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QHeaderView
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


connection = sqlite3.connect("coffee.db")
cursor = connection.cursor()


class Ui_CreateCoffee(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(215, 219)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 31, 21))
        self.label.setObjectName("label")
        self.sort_box = QtWidgets.QComboBox(Form)
        self.sort_box.setGeometry(QtCore.QRect(70, 10, 131, 21))
        self.sort_box.setObjectName("sort_box")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 61, 21))
        self.label_2.setObjectName("label_2")
        self.fry_box = QtWidgets.QComboBox(Form)
        self.fry_box.setGeometry(QtCore.QRect(70, 40, 131, 21))
        self.fry_box.setObjectName("fry_box")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 61, 21))
        self.label_3.setObjectName("label_3")
        self.type_box = QtWidgets.QComboBox(Form)
        self.type_box.setGeometry(QtCore.QRect(70, 70, 131, 21))
        self.type_box.setObjectName("type_box")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 61, 21))
        self.label_4.setObjectName("label_4")
        self.taste_box = QtWidgets.QComboBox(Form)
        self.taste_box.setGeometry(QtCore.QRect(70, 100, 131, 21))
        self.taste_box.setObjectName("taste_box")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 61, 21))
        self.label_5.setObjectName("label_5")
        self.price_edit = QtWidgets.QDoubleSpinBox(Form)
        self.price_edit.setGeometry(QtCore.QRect(70, 130, 131, 22))
        self.price_edit.setMaximum(9999999999.0)
        self.price_edit.setObjectName("price_edit")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 160, 31, 21))
        self.label_6.setObjectName("label_6")
        self.volume_edit = QtWidgets.QSpinBox(Form)
        self.volume_edit.setGeometry(QtCore.QRect(70, 160, 131, 22))
        self.volume_edit.setMinimum(0)
        self.volume_edit.setMaximum(999999999)
        self.volume_edit.setProperty("value", 0)
        self.volume_edit.setObjectName("volume_edit")
        self.save_btn = QtWidgets.QPushButton(Form)
        self.save_btn.setGeometry(QtCore.QRect(130, 190, 75, 21))
        self.save_btn.setObjectName("save_btn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Сорт:"))
        self.label_2.setText(_translate("Form", "Обжарка:"))
        self.label_3.setText(_translate("Form", "Тип:"))
        self.label_4.setText(_translate("Form", "Вкус"))
        self.label_5.setText(_translate("Form", "Цена:"))
        self.label_6.setText(_translate("Form", "Обьем"))
        self.save_btn.setText(_translate("Form", "Сохранить"))


class Ui_AllCoffeesView(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(680, 331)
        self.coffee_table_data = QtWidgets.QTableWidget(Form)
        self.coffee_table_data.setGeometry(QtCore.QRect(10, 40, 661, 281))
        self.coffee_table_data.setObjectName("coffee_table_data")
        self.coffee_table_data.setColumnCount(0)
        self.coffee_table_data.setRowCount(0)
        self.add_coffee_btn = QtWidgets.QPushButton(Form)
        self.add_coffee_btn.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.add_coffee_btn.setObjectName("add_coffee_btn")
        self.edit_coffee_btn = QtWidgets.QPushButton(Form)
        self.edit_coffee_btn.setGeometry(QtCore.QRect(90, 10, 75, 23))
        self.edit_coffee_btn.setObjectName("edit_coffee_btn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Кофе"))
        self.add_coffee_btn.setText(_translate("Form", "Добавить"))
        self.edit_coffee_btn.setText(_translate("Form", "Изменить"))


class CreateCoffee(QWidget, Ui_CreateCoffee):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.replace_id = None
        self.initUI()

    def initUI(self):
        self.setFixedSize(215, 219)
        self.save_btn.clicked.connect(self.save)
        sorts = map(lambda x: x[0], cursor.execute("SELECT name FROM sorts").fetchall())
        fries = map(lambda x: x[0], cursor.execute("SELECT name FROM fry").fetchall())
        types = map(lambda x: x[0], cursor.execute("SELECT name FROM types").fetchall())
        tastes = map(lambda x: x[0], cursor.execute("SELECT description FROM tastes").fetchall())
        self.sort_box.addItems(sorts)
        self.fry_box.addItems(fries)
        self.type_box.addItems(types)
        self.taste_box.addItems(tastes)

    def save(self):
        sort = self.sort_box.currentIndex() + 1
        fry = self.fry_box.currentIndex() + 1
        type_name = self.type_box.currentIndex() + 1
        taste = self.taste_box.currentIndex() + 1
        price = self.price_edit.value()
        volume = self.volume_edit.value()
        if price and volume:
            if self.replace_id:
                cursor.execute("DELETE FROM coffees WHERE id=?", (self.replace_id, ))
            cursor.execute("INSERT INTO coffees(sort, fry, type, taste, price, volume) "
                           "VALUES(?, ?, ?, ?, ?, ?)", (sort, fry, type_name, taste,
                                                        price, volume))
            connection.commit()
            window.load_coffee_data()
            self.close()


class AllCoffeesView(QWidget, Ui_AllCoffeesView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.coffee_creation_form = CreateCoffee()
        self.setFixedSize(680, 331)
        self.add_coffee_btn.clicked.connect(self.add_coffee)
        self.edit_coffee_btn.clicked.connect(self.edit_coffee)
        self.coffee_table_data.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.load_coffee_data()

    def load_coffee_data(self):
        query_result = cursor.execute(f"SELECT "
                                      f"coffees.id, sorts.name, fry.name, types.name, tastes.description,"
                                      f"coffees.price, coffees.volume "
                                      f"FROM coffees "
                                      f"INNER JOIN sorts ON sorts.id = coffees.sort "
                                      f"INNER JOIN fry ON fry.id = coffees.fry "
                                      f"INNER JOIN types ON types.id = coffees.type "
                                      f"INNER JOIN tastes ON tastes.id = coffees.taste "
                                      ).fetchall()
        self.coffee_table_data.setRowCount(len(query_result))
        self.coffee_table_data.setColumnCount(len(query_result[0]))
        titles = ["ID", "Сорт", "Обжарка", "Тип", "Вкус", "Цена(рубли)", "Обьем(см3)"]
        self.coffee_table_data.setHorizontalHeaderLabels(titles)

        for i, elem in enumerate(query_result):
            for j, val in enumerate(elem):
                self.coffee_table_data.setItem(i, j, QTableWidgetItem(str(val)))
        self.coffee_table_data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def add_coffee(self):
        self.coffee_creation_form.setWindowTitle("Добавление кофе")
        self.coffee_creation_form.replace_id = None
        self.coffee_creation_form.show()

    def edit_coffee(self):
        row = self.coffee_table_data.currentRow()
        if row == -1:
            return
        self.coffee_creation_form.setWindowTitle("Изменение кофе")
        self.coffee_creation_form.replace_id = int(self.coffee_table_data.item(row, 0).text())
        self.coffee_creation_form.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    window = AllCoffeesView()
    window.show()
    sys.exit(app.exec())

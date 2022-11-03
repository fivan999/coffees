from random import randint
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QHeaderView
from PyQt5 import uic
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


connection = sqlite3.connect("coffee.db")
cursor = connection.cursor()


class CreateCoffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
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


class AllCoffeesView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setWindowTitle("Кофе")
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
        print(query_result)
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

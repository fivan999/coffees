from random import randint
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import uic
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


connection = sqlite3.connect("coffee.db")
cursor = connection.cursor()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.load_coffee_data()

    def load_coffee_data(self):
        query_result = cursor.execute(f"SELECT "
                                      f"coffees.id, sorts.name, fry.name, types.name, tastes.description,"
                                      f"coffees.price, coffees.volume "
                                      f"FROM coffees "
                                      f"INNER JOIN sorts ON sorts.id = coffees.sort"
                                      f"INNER JOIN fry.id = coffees.fry"
                                      f"INNER JOIN types.id = coffees.type"
                                      f"INNER JOIN tastes.id = coffees.taste "
                                      ).fetchall()

        self.film_table_data.setRowCount(len(query_result))
        self.film_table_data.setColumnCount(len(query_result[0]))
        titles = ["ID", "Сорт", "Обжарка", "Тип", "Вкус", "Цена(рубли)", "Обьем(см3)"]
        self.film_table_data.setHorizontalHeaderLabels(titles)

        for i, elem in enumerate(query_result):
            for j, val in enumerate(elem):
                self.film_table_data.setItem(i, j, QTableWidgetItem(str(val)))
                # self.film_table_data.item(i, j).setFlags(QtCore.Qt.ItemIsEnabled)
        self.film_table_data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    window = Window()
    window.show()
    sys.exit(app.exec())

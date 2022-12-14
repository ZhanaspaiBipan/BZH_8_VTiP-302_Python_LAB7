#!/usr/bin/env python3
# coding=utf-8
import random
import sys
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QButtonGroup
from PyQt5.QtCore import QTimer, QRect

answers = ['', '', '']  # 1 - form2, 2 - form3, 3 - form4


class Form1(QtWidgets.QMainWindow):
    # аргумент str говорит о том, что сигнал должен быть сторокового типа
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form1, self).__init__()
        uic.loadUi('uis/form1.ui', self)

        self.setWindowTitle('Приветствие')

        self.x = 50  # 477
        self.y = 13
        self.label_welcome_1.move(self.x, self.y)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_label_left)
        self.timer.start(10)  # 100

        self.btn_exit.clicked.connect(self.close)
        self.btn_begin.clicked.connect(self.next)

    def move_label_left(self):
        if self.x <= -150:  # 477
            self.x = self.width()  # 477
            self.x -= 1
            self.label_welcome_1.move(self.x, self.height() - 30)
        else:
            self.x -= 1
            self.label_welcome_1.move(self.x, self.y)
        self.label_welcome_1.adjustSize()

    def next(self):
        self.switch_window.emit('1>2')


class Form2(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form2, self).__init__()
        uic.loadUi('uis/form2.ui', self)

        self.setWindowTitle('Детство')
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))
        self.label_img.setPixmap(QPixmap('images/hobby.png'))
        self.label_img.setScaledContents(True)

        # запрещаем редактирование таблицы
        #        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.btn_back.clicked.connect(self.back)
        self.btn_next.clicked.connect(self.next)



    def back(self):
        self.switch_window.emit('1<2')

    def next(self):
        self.switch_window.emit('2>3')
        answers[1] = self.tableWidget.item(0, 0).text()


class Form3(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    # Смена картинок

    def __init__(self):
        super(Form3, self).__init__()
        uic.loadUi('uis/form3.ui', self)

        self.setWindowTitle('Юность')

        self.label_img.setPixmap(QPixmap('images/sun.png'))

        self.label_img.setScaledContents(True)

        if answers[0] is not None:
            self.label_selected.setText('Выбрано: ' + answers[0])

        self.button_group = QButtonGroup()

        self.button_group.addButton(self.checkBox_1, 1)
        self.button_group.addButton(self.checkBox_2, 2)
        self.button_group.addButton(self.checkBox_3, 3)
        self.button_group.addButton(self.checkBox_4, 4)

        self.checkBox_1.stateChanged.connect(
            lambda: self.onToggled(self.checkBox_1, 'images/sun.png'))
        self.checkBox_2.stateChanged.connect(
            lambda: self.onToggled(self.checkBox_2, 'images/rain.png'))
        self.checkBox_3.stateChanged.connect(
            lambda: self.onToggled(self.checkBox_3, 'images/cloud.png'))
        self.checkBox_4.stateChanged.connect(
            lambda: self.onToggled(self.checkBox_4, 'images/another.png'))

        self.btn_back.clicked.connect(self.back)
        self.btn_next.clicked.connect(self.next)

    def onToggled(self, checkbox, image):
        if checkbox.isChecked():
            answers[0] = checkbox.text()
            self.label_selected.setText('Выбрано: ' + answers[0])
            self.label_img.setPixmap(QPixmap(image))

    def back(self):
        self.switch_window.emit('2<3')

    def next(self):
        self.switch_window.emit('3>4')

class Form4(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form4, self).__init__()
        uic.loadUi('uis/form4.ui', self)

        self.setWindowTitle('Отрочество')


        self.label_img.setPixmap(QPixmap('images/toys.png'))
        self.label_img.setScaledContents(True)

        if answers[0] is not None:
            self.label_selected.setText('Выбрано: ' + answers[0])

        self.listWidget.clicked.connect(self.listWidget_clicked)
        self.btn_back.clicked.connect(self.back)
        self.btn_next.clicked.connect(self.next)

        self.listWidget.setCurrentRow(0)
        self.listWidget_clicked()

    def listWidget_clicked(self):
       answers[2] = self.listWidget.currentItem().text()
       self.label_selected.setText('Выбрано: ' + answers[2])

    def back(self):
        self.switch_window.emit('3<4')

    def next(self):
        self.switch_window.emit('4>5')

class Form5(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form5, self).__init__()
        uic.loadUi('uis/form5.ui', self)

        self.setWindowTitle('Результат')
        # присваиваем значение ячейкам таблицы

        self.lineEdit.insert(answers[2])
        self.lineEdit_2.insert(answers[1])
        self.lineEdit_3.insert(answers[0])

        self.btn_back.clicked.connect(self.back)
        self.btn_exit.clicked.connect(self.close)

    def back(self):
        self.switch_window.emit("4<5")


'''
Класс управления переключения окон
'''


class Controller:
    def __init__(self):
        pass

    def select_forms(self, text):
        if text == '1':
            self.form1 = Form1()
            self.form1.switch_window.connect(self.select_forms)
            self.form1.show()

        if text == '1>2':
            self.form2 = Form2()
            self.form2.switch_window.connect(self.select_forms)
            self.form2.show()
            self.form1.close()

        if text == '2>3':
            self.form3 = Form3()
            self.form3.switch_window.connect(self.select_forms)
            self.form3.show()
            self.form2.close()

        if text == '3>4':
            self.form4 = Form4()
            self.form4.switch_window.connect(self.select_forms)
            self.form4.show()
            self.form3.close()

        if text == '4>5':
            self.form5 = Form5()
            self.form5.switch_window.connect(self.select_forms)
            self.form5.show()
            self.form4.close()

        if text == '4<5':
            self.form4 = Form4()
            self.form4.switch_window.connect(self.select_forms)
            self.form4.show()
            self.form5.close()

        if text == '3<4':
            self.form3 = Form3()
            self.form3.switch_window.connect(self.select_forms)
            self.form3.show()
            self.form4.close()

        if text == '2<3':
            self.form2 = Form2()
            self.form2.switch_window.connect(self.select_forms)
            self.form2.show()
            self.form3.close()

        if text == '1<2':
            self.form1 = Form1()
            self.form1.switch_window.connect(self.select_forms)
            self.form1.show()
            self.form2.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.select_forms("1")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

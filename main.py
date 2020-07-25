import os
import sys

import numpy as np
from pandas import read_csv, isna
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QInputDialog, QLabel,
    QHBoxLayout, QVBoxLayout, QGridLayout, QErrorMessage
)

from utils import *

name2num = {
    # TODO korean, english, japanese
}


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()

        self.index = 74
        self.idol_index = 0
        self.csv = read_csv('data/korean.csv')
        self.texts = self.csv.iloc[:, :6]

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Title')

        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel('Input1'), 0, 0)
        grid.addWidget(QLabel('Input2'), 1, 0)
        grid.addWidget(QLabel('Buttons'), 2, 0)
        grid.addWidget(QLabel('Texts'), 3, 0)

        self.input1_box = QLineEdit('아이돌_번호 혹은 이름')
        grid.addWidget(self.input1_box, 0, 1)

        self.btn_save1 = QPushButton('Set', self)
        self.btn_save1.clicked.connect(self.find_idol)
        grid.addWidget(self.btn_save1, 0, 2)

        self.input_box = QLineEdit('커뮤이름')
        # self.input_box.resize(100, 100)
        grid.addWidget(self.input_box, 1, 1)

        self.btn_save = QPushButton('Set', self)
        self.btn_save.clicked.connect(self.find_title)
        grid.addWidget(self.btn_save, 1, 2)

        self.label_jp = QLabel('jp', self)
        grid.addWidget(self.label_jp, 3, 1)

        self.label_kr = QLabel('kr', self)
        grid.addWidget(self.label_kr, 3, 2)

        self.btn_before = QPushButton('Before', self)
        self.btn_before.clicked.connect(self.showBefore)
        self.btn_next = QPushButton('Next', self)
        self.btn_next.clicked.connect(self.showNext)

        grid.addWidget(self.btn_before, 2, 1)
        grid.addWidget(self.btn_next, 2, 2)

        # shows default text
        self.index = 1
        self.showText()

        self.setMinimumSize(300, 120)
        self.setMaximumSize(600, 200)
        self.move(300, 300)
        self.resize(500, 150)
        self.show()

    def showText(self):
        print(self.index, self.idol_index)
        text_jp, text_kr = self.get_labels_from_index(self.index)

        self.label_jp.setText(text_jp)
        self.label_kr.setText(text_kr)

    def showBefore(self):
        self.index -= 1
        if self.index <= 1:
            self.index = 1
        self.showText()

    def showNext(self):
        self.index += 1
        if self.index >= len(self.texts):
            self.index = 1
        self.showText()

    def get_labels_from_index(self, row):
        text_jp = self.texts.iloc[row, 3]

        # search for next text
        while isna(text_jp):
            row = row + 1
            text_jp = self.texts.iloc[row, 4]
            if row >= len(self.texts):
                row = 0

        text_kr = self.texts.iloc[row, 4]
        return text_jp, text_kr

    def set_texts_from_idol_index(self):
        start = 5 * self.idol_index
        end = 5 * self.idol_index + 4
        self.texts = self.csv.iloc[:, start:end + 1]

    def find_title(self):
        self.title = self.input_box.text()

        self.titles = self.texts.iloc[:, 0]
        if self.titles is None:
            pass

        title = self.input_box.text()
        title = title.replace('\\', '\\\\')

        matches = self.titles.str.contains(title, na=False)
        index = matches.idxmax()
        self.index = index + 2
        self.showText()

    def find_idol(self):
        try:
            self.idol_index = int(self.input1_box.text())
        except Exception as e1:
            try:
                self.idol_index = name_text_to_num(self.input1_box.text(), 'en')
            except Exception as e2:  # TODO show error window
                error_dialog = QErrorMessage()
                error_dialog.setWindowTitle('Error')
                error_dialog.showMessage(e1, e2)
                error_dialog.setMinimumSize(200, 150)
                error_dialog.resize(200, 200)
                error_dialog.exec_()

        self.set_texts_from_idol_index()

        self.index = 0
        # self.find_title()
        self.title = 5 * self.idol_index + 1  # Todo just use column, not writing a new row containing it
        self.titles = self.texts.iloc[self.title]

        self.showText()


def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    '''
    csv = pd.read_csv('data/korean.csv')
    aa = csv.head(150)
    bb = aa.iloc[:, :5]
    print(list(bb))
    #cc = bb['Unnamed: 1']
    cc = bb['#FILENAME: P\SR-1\ショッピング日和.csv'] #TODO change column name by changing data

    start = cc[cc=='#FILENAME: P\SR-1\感謝を形に.csv'].index.tolist()[0]
    text = cc[start:] #TODO loading 1000 lines should be fine
    end = text[text=='#EOF'].index.tolist()[0]
    print(start)
    print(end)
    print(bb.iloc[74]['Unnamed: 3'])
    '''


if __name__ == '__main__':
    main()

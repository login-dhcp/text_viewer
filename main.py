import os
import sys
import pkg_resources.py2_warn
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (
	QApplication, QWidget, QPushButton, QLineEdit, QInputDialog, QLabel,
	QHBoxLayout, QVBoxLayout, QGridLayout
)


class App(QWidget):
	def __init__(self):
		super(App, self).__init__()

		self.index = 74
		csv = pd.read_csv('data/korean.csv')
		self.text = csv.iloc[:, :5]

		self.initUI()

	def initUI(self):
		self.setWindowTitle('Title')

		grid = QGridLayout()
		self.setLayout(grid)

		grid.addWidget(QLabel('Input'), 0, 0)
		grid.addWidget(QLabel('Buttons'), 1, 0)
		grid.addWidget(QLabel('Texts'), 2, 0)

		self.input_box = QLineEdit('커뮤이름')
		# self.input_box.resize(100, 100)
		grid.addWidget(self.input_box, 0, 1)
		self.btn_save = QPushButton('Set', self)
		self.btn_save.clicked.connect(self.find_idx)
		grid.addWidget(self.btn_save, 0, 2)

		self.label_jp = QLabel('jp', self)
		grid.addWidget(self.label_jp, 2, 1)
		self.label_kr = QLabel('kr', self)
		grid.addWidget(self.label_kr, 2, 2)

		self.btn_before = QPushButton('Before', self)
		self.btn_before.clicked.connect(self.showBefore)
		self.btn_next = QPushButton('Next', self)
		self.btn_next.clicked.connect(self.showNext)

		grid.addWidget(self.btn_before, 1, 1)
		grid.addWidget(self.btn_next, 1, 2)

		self.showIndex(74)

		self.move(300, 300)
		self.resize(500, 100)
		self.show()

	def showText(self):
		text_jp = self.text.iloc[self.index]['Unnamed: 3']
		if pd.isna(text_jp):
			self.index = 1
			text_jp = self.text.iloc[self.index]['Unnamed: 3']
		text_kr = self.text.iloc[self.index]['Unnamed: 4']

		self.label_jp.setText(text_jp)
		self.label_kr.setText(text_kr)

	def showIndex(self, index):
		self.index = index
		self.showText()

	def showBefore(self):
		self.index -= 1
		if self.index <= 1:
			self.index = 1
		self.showText()

	def showNext(self):
		self.index += 1
		if self.index >= len(self.text):
			self.index = 1
		self.showText()

	def find_idx(self):
		title = '#FILENAME: ' + self.input_box.text() + '.csv'
		titles = self.text['#FILENAME: P\SR-1\ショッピング日和.csv']
		index = titles[titles == title].index.tolist()
		if len(index) == 0:
			print('none')
		else:
			print(index)
			self.index = index[0] + 2
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

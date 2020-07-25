import os
import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (
	QApplication, QWidget, QPushButton, QLineEdit, QInputDialog, QLabel,
	QHBoxLayout, QVBoxLayout, QGridLayout, QErrorMessage
)

name2num = {
	#TODO korean, english, japanese
}


class App(QWidget):
	def __init__(self):
		super(App, self).__init__()

		self.index = 74
		self.idol_index = 1
		self.csv = pd.read_csv('data/korean.csv')
		self.text = self.csv.iloc[:, :5]

		self.initUI()

	def initUI(self):
		self.setWindowTitle('Title')

		grid = QGridLayout()
		self.setLayout(grid)

		grid.addWidget(QLabel('Input1'), 0, 0)
		grid.addWidget(QLabel('Input2'), 1, 0)
		grid.addWidget(QLabel('Buttons'), 2, 0)
		grid.addWidget(QLabel('Texts'), 3, 0)

		self.input1_box = QLineEdit('아이돌_번호')
		grid.addWidget(self.input1_box, 0, 1)

		self.btn_save1 = QPushButton('Set', self)
		self.btn_save1.clicked.connect(self.find_idol)
		grid.addWidget(self.btn_save1, 0, 2)

		self.input_box = QLineEdit('커뮤이름')
		# self.input_box.resize(100, 100)
		grid.addWidget(self.input_box, 1, 1)

		self.btn_save = QPushButton('Set', self)
		self.btn_save.clicked.connect(self.find_idx)
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

		self.showIndex(0)

		self.setMinimumSize(300, 120)
		self.setMaximumSize(600, 200)
		self.move(300, 300)
		self.resize(500, 150)
		self.show()

	def showText(self):
		print(self.idol_index, self.index)
		text_jp = self.text.iloc[self.index]['%d'%(5*self.idol_index-1)]
		if pd.isna(text_jp):
			self.index = 1
			text_jp = self.text.iloc[self.index]['%d'%(5*self.idol_index-1)]
		text_kr = self.text.iloc[self.index]['%d'%(5*self.idol_index)]

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
		self.title = '#FILENAME: ' + self.input_box.text() + '.csv' #TODO do not use this... using comu_id is much better
		if self.titles is None:
			print('titles are wrong')
			#self.titles = self.text['#FILENAME: P\SR-1\ショッピング日和.csv']
			self.titles = self.text['%d'%(5*self.idol_index-4)]
		index = self.titles[self.titles == self.title].index.tolist()
		if len(index) == 0:
			print('none')
		else:
			print(index)
			self.index = index[0] + 2
		self.showText()


	def find_idol(self):
		try:
			self.idol_index = int(self.input1_box.text())
		except ValueError as e:
			#try:
				#idol_name = self.input1_box.text #TODO
			#except:
			error_dialog = QErrorMessage()
			error_dialog.setWindowTitle('Error')
			error_dialog.showMessage('input valid name/number')
			error_dialog.setMinimumSize(200, 150)
			error_dialog.resize(200, 200)

			error_dialog.exec_()
			self.idol_index = 1


		start = 5 * (self.idol_index-1)
		end = 5 * self.idol_index
		self.text = self.csv.iloc[:, start:end]

		self.index = 0
		#self.find_idx()
		self.title = '%d'%(5*self.idol_index-4) #Todo just use colnum, not writing a new row containing it
		self.titles = self.text[self.title]

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

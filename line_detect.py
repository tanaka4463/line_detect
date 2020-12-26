# QMainwindowで作成
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QMessageBox
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import cv2
import numpy as np
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 1000, 1000)
        self.put_menubar()

        self.window = QWidget()
        self.setCentralWidget(self.window)
        self.hbox = QtWidgets.QHBoxLayout()
        self.window.setLayout(self.hbox)

        self.imgcanvas = pg.GraphicsLayoutWidget()
        self.imgcanvas.setFixedWidth(1260)
        self.view = self.imgcanvas.addViewBox()
        self.view.setAspectLocked(True)
        self.imgitem = pg.ImageItem()
        self.imgitem.rotate(-90)
        self.view.addItem(self.imgitem)
        self.hbox.addWidget(self.imgcanvas)
        self.grid = QtWidgets.QGridLayout()
        
        self.hbox.addLayout(self.grid)
        self.label1 = QtWidgets.QLabel('rho')
        self.label2 = QtWidgets.QLabel('theta')
        self.label3 = QtWidgets.QLabel('threshold')
        self.label4 = QtWidgets.QLabel('minLineLength')
        self.label5 = QtWidgets.QLabel('maxLineGap')
        self.textbox1 = QtWidgets.QLineEdit('1') # rho
        self.textbox2 = QtWidgets.QLineEdit('360') # theta
        self.textbox3 = QtWidgets.QLineEdit('100') # threshold
        self.textbox4 = QtWidgets.QLineEdit('100') # minLineLength
        self.textbox5 = QtWidgets.QLineEdit('5') # maxLineGap
        self.button1 = QtWidgets.QPushButton('run')
      
        self.slider1 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider1.setRange(0, 360)
        self.slider1.setValue(100)
        self.slider2 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider2.setRange(0, 200)
        self.slider2.setValue(100)
        self.slider3 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider3.setRange(0, 100)
        self.slider3.setValue(5)
        self.grid.addWidget(self.label1, 0, 0)
        self.grid.addWidget(self.label2, 1, 0)
        self.grid.addWidget(self.label3, 2, 0)
        self.grid.addWidget(self.label4, 4, 0)
        self.grid.addWidget(self.label5, 6, 0)
        self.grid.addWidget(self.textbox1, 0, 1)
        self.grid.addWidget(self.textbox2, 1, 1)
        self.grid.addWidget(self.textbox3, 2, 1)
        self.grid.addWidget(self.textbox4, 4, 1)
        self.grid.addWidget(self.textbox5, 6, 1)
        self.grid.addWidget(self.slider1,  3, 0, 1, 2)
        self.grid.addWidget(self.slider2,  5, 0, 1, 2)
        self.grid.addWidget(self.slider3,  7, 0, 1, 2)
        self.grid.addWidget(self.button1, 8, 0, 1, 2) 

        self.button1.clicked.connect(self.run)  
        self.slider1.valueChanged.connect(self.threshold_change)
        self.slider2.valueChanged.connect(self.minLineLength_change)
        self.slider3.valueChanged.connect(self.maxLineGap_change)

    def put_menubar(self):
        self.menubar = self.menuBar()
        self.filemenu = self.menubar.addMenu('File')
    # actionのインスタンス
        self.new_act = QtWidgets.QAction('new')
        self.filemenu.addAction(self.new_act)
        self.new_act.triggered.connect(self.fileopen)
    
    def fileopen(self):
        self.filepath = QtWidgets.QFileDialog.getOpenFileName(self, 'open file', os.getcwd())
        self.img = cv2.imread(self.filepath[0]) # self.imgは常にBGR形式とする
        self.color_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.pixmap_img = QtGui.QPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(self.filepath[0])))
        self.qimg = QtGui.QImage(self.filepath[0])
        self.imgitem.setImage(self.color_img)

    def run(self):
        self.color_img_copy = self.color_img.copy()
        self.gray = cv2.cvtColor(self.color_img_copy, cv2.COLOR_RGB2GRAY)
        self.th = cv2.bitwise_not(self.gray)
        self.lines = cv2.HoughLinesP(self.th, rho = int(self.textbox1.text()), theta = np.pi / int(self.textbox2.text()), 
                                              threshold = int(self.textbox3.text()), minLineLength = int(self.textbox4.text()), maxLineGap = int(self.textbox5.text()))
        try:
            for line in self.lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(self.color_img_copy, (x1, y1), (x2, y2), (0, 0, 255), 3)
        except:
            QMessageBox.warning(None, 'error', 'error', QMessageBox.Yes)
        self.imgitem.setImage(self.color_img_copy)

    def threshold_change(self, value):
        self.textbox3.setText(str(value))
        self.color_img_copy = self.color_img.copy()
        self.gray = cv2.cvtColor(self.color_img_copy, cv2.COLOR_RGB2GRAY)
        self.th = cv2.bitwise_not(self.gray)
        self.lines = cv2.HoughLinesP(self.th, rho = int(self.textbox1.text()), theta = np.pi / int(self.textbox2.text()), 
                                              threshold = int(self.textbox3.text()), minLineLength = int(self.textbox4.text()), maxLineGap = int(self.textbox5.text()))
        try:
            for line in self.lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(self.color_img_copy, (x1, y1), (x2, y2), (0, 0, 255), 3)
        except:
            QMessageBox.warning(None, 'error', 'error', QMessageBox.Yes)
        self.imgitem.setImage(self.color_img_copy)

    def minLineLength_change(self, value):
        self.textbox4.setText(str(value))
        self.color_img_copy = self.color_img.copy()
        self.gray = cv2.cvtColor(self.color_img_copy, cv2.COLOR_RGB2GRAY)
        self.th = cv2.bitwise_not(self.gray)
        self.lines = cv2.HoughLinesP(self.th, rho = int(self.textbox1.text()), theta = np.pi / int(self.textbox2.text()), 
                                              threshold = int(self.textbox3.text()), minLineLength = int(self.textbox4.text()), maxLineGap = int(self.textbox5.text()))
        try:
            for line in self.lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(self.color_img_copy, (x1, y1), (x2, y2), (0, 0, 255), 3)
        except:
            QMessageBox.warning(None, 'error', 'error', QMessageBox.Yes)
        self.imgitem.setImage(self.color_img_copy)

    def maxLineGap_change(self, value):
        self.textbox5.setText(str(value))
        self.color_img_copy = self.color_img.copy()
        self.gray = cv2.cvtColor(self.color_img_copy, cv2.COLOR_RGB2GRAY)
        self.th = cv2.bitwise_not(self.gray)
        self.lines = cv2.HoughLinesP(self.th, rho = int(self.textbox1.text()), theta = np.pi / int(self.textbox2.text()), 
                                              threshold = int(self.textbox3.text()), minLineLength = int(self.textbox4.text()), maxLineGap = int(self.textbox5.text()))
        try:
            for line in self.lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(self.color_img_copy, (x1, y1), (x2, y2), (0, 0, 255), 3)
        except:
            QMessageBox.warning(None, 'error', 'error', QMessageBox.Yes)
        self.imgitem.setImage(self.color_img_copy)       

def main():
    app = QtGui.QApplication(sys.argv)
    plot = MainWindow()
    plot.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()        
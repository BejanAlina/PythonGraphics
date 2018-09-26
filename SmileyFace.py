# -*- coding: utf-8 -*-

import sys
from PySide2 import QtCore, QtWidgets, QtGui


class SmileyFace(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(100, 100, 700, 600)
        self.setWindowTitle('Draw circles')
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-image: url(background.jpg);")
        self.initWindow()


    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        # make a black drawing background
        paint.setBrush(QtCore.Qt.black)
        paint.drawRect(event.rect())
        # draw cyan circles with cyan borders
        paint.setPen(QtCore.Qt.cyan)
        paint.setBrush(QtCore.Qt.cyan)

        elipse1 = paint.drawEllipse(QtCore.QRect(50, 100, 200, 200));
        elipse2 = paint.drawEllipse(QtCore.QRect(450, 100, 200, 200));
        paint.end()

    def initWindow(self):

        self.button = QtWidgets.QPushButton("Start", self)
        self.button.setIcon(QtGui.QIcon('Button-Cyan.png'))
        self.button.move(30,30)
        self.button.clicked.connect(self.doAnimation)

        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Raised)
        self.frame.setGeometry(550,450,100,100)
        self.frame.setStyleSheet('background-color: cyan; border: 1px solid black; border-radius: 20px;')

    def doAnimation(self):
        self.anim = QtCore.QPropertyAnimation(self.frame, b"geometry")
        self.anim.setDuration(10000)
        self.anim.setStartValue(QtCore.QRect(0,0,100,100))
        self.anim.setEndValue(QtCore.QRect(290,290,100,100))
        self.anim.start()


app = QtWidgets.QApplication(sys.argv)
circles = SmileyFace()
circles.show()
sys.exit(app.exec_())

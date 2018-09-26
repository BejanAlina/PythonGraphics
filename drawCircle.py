import sys

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt, QPoint, QRectF


class SmileyFace(QtWidgets.QWidget):
    centerPoint = 0
    radx = 100  # for circle make the ellipse radius match
    isHappy = True

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Draw circles')
        self.centerPoint = self.height() / 2
        self.radx = self.centerPoint / 3
        # robocop states & buttons
        self.statesArray = ["I'm Happy", "I'm Saaaaad :( "]
        self.button = QtWidgets.QPushButton("Bye!")
        self.text = QtWidgets.QLabel("Hello")
        self.text.setStyleSheet('color: white; font-size: 22pt')
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.toggleState)

    def resizeEvent(self, event):
        self.centerPoint = self.height() / 2
        self.radx = self.centerPoint / 3
        self.paintEvent(self)

    def toggleState(self):
        self.isHappy = not self.isHappy
        self.paintEvent(self)

    def paintEvent(self, event):
        # init values
        center = QPoint(self.centerPoint, self.centerPoint)
        radius = self.radx / 2

        # cadran II center point Y
        centerCad2Y = self.centerPoint - radius

        # cadran I center point X
        centerCad1X = self.centerPoint + radius
        eyeLeftCenter = QPoint(centerCad2Y, centerCad2Y)
        eyeRightCenter = QPoint(centerCad1X, centerCad2Y)

        # arc rectangles
        rectangleSad = QRectF(centerCad2Y, self.centerPoint, self.radx, self.radx)
        rectangleSmile = QRectF(
            self.centerPoint - radius,
            self.centerPoint - radius,
            self.radx,
            self.radx
        )

        startAngleSad = 16
        spanAngle = 180 * 16

        paint = QtGui.QPainter()
        paint.begin(self)
        # background
        pixmap = QtGui.QPixmap('background.jpg')
        paint.drawPixmap(event.rect(), pixmap)

        # optional but why not
        paint.setRenderHint(QtGui.QPainter.Antialiasing)

        # make a white drawing background
        paint.setBrush(Qt.white)

        # draw red circles
        paint.setPen(Qt.red)

        # optionally fill each circle yellow
        paint.setBrush(Qt.yellow)
        paint.drawEllipse(center, self.radx, self.radx)
        paint.setBrush(Qt.black)

        # draw eyes
        eyeRadius = self.radx / 7
        paint.drawEllipse(eyeLeftCenter, eyeRadius, eyeRadius)
        paint.drawEllipse(eyeRightCenter, eyeRadius, eyeRadius)

        # draw smile line
        paint.setPen(QtGui.QPen(Qt.black))  # <-- arc color

        # check robocop states & display
        if not self.isHappy:
            # make smiley sad :(
            paint.drawArc(rectangleSad, startAngleSad, spanAngle)
            self.text.setText(self.statesArray[1])
            self.button.setText("Hello!")
        else:
            paint.drawArc(rectangleSmile, -startAngleSad, -spanAngle)
            self.text.setText(self.statesArray[0])
            self.button.setText("Bye!")

        paint.end()


app = QtWidgets.QApplication(sys.argv)
circles = SmileyFace()
circles.show()
sys.exit(app.exec_())

import os

from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QPushButton, QApplication


class RepeatTimer(QtCore.QTimer):
    timeoutCounter = QtCore.Signal(int)
    endRepeat = QtCore.Signal()

    def __init__(self, numberOfRepeats = 1, delay=10):
        QtCore.QTimer.__init__(self)
        self.__numberOfRepeats = 1
        self.numberOfRepeats = numberOfRepeats

        self.__delay = 10
        self.delay = delay

        self.__internalCounter = 0

        self.timeout.connect(self.__eval)

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, value):
        if value >= 0 and type(value).__name__ == "int":
            self.__delay = value
            self.setInterval(value)

    @property
    def numberOfRepeats(self):
        return self.__numberOfRepeats

    @numberOfRepeats.setter
    def numberOfRepeats(self, value):
        if value >= 0 and type(value).__name__ == "int":
            self.__numberOfRepeats = value

    def __eval(self):
        if self.__internalCounter >= self.__numberOfRepeats - 1:
            self.stop()
            self.endRepeat.emit()
            self.timeoutCounter.emit(self.__internalCounter)
            self.__internalCounter = 0
        else:
            self.timeoutCounter.emit(self.__internalCounter)
            self.__internalCounter += 1


class AnimButton(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)

        ## The frames used for the animation
        self.__frames = None
        ## The dfolder of the frames
        self.__basePath = None
        ## Thee paths of the frames
        self.__framesPath = None
        ## The size of the frames, it's automatically extracted from the first frame
        self.__framesSize = None
        ## How many frames in the animation
        self.__numberOfFrames = None
        ## The internal timer for the swap of the frames
        self._timer = RepeatTimer(10, 100)

        self.clicked.connect(self.playAnim)
        self._timer.timeoutCounter.connect(self._setFrame)

    def setFrames(self, basePath, frames=[], resizeButton=True, speed=41):
        self.__frames = self._convertFrame(basePath, frames, resizeButton, speed)
        self._setFrame(0)

    def _convertFrame(self, basePath, frames=[], resizeButton=True, speed=41):

        processed = []

        ## lets loop the frames
        for i, f in enumerate(frames):
            ## convert the frame to pix map
            pix = QtGui.QPixmap(basePath + "/" + f)

            ## if it is the first frame extract the size
            if i == 0:
                self.__framesSize = pix.size()

            ## convert to QIcon
            im = QtGui.QIcon(pix)
            processed.append(im)

        ## store some parameters
        self.__numberOfFrames = len(processed)
        self.__basePath = basePath
        self.__framesPath = frames

        ## Set the kick off of the times based on the number of frames
        self._timer.numberOfRepeats = self.__numberOfFrames
        ## Set the delay of the timer
        self._timer.delay = speed

        ## if required set the button size equal to frame size
        if resizeButton == 1:
            self.setGeometry(0, 0, self.__framesSize.width(), self.__framesSize.height())

        return processed

    def _setFrame(self, index=0):
        if (self.__frames and self.__framesSize and index <= (self.__numberOfFrames - 1)) == True:
            self.setIcon(self.__frames[index])
            self.setIconSize(self.__framesSize)

    def _setFrameData(self, data):
        self.__frames = data

    def playAnim(self):
        self._timer.start()

def main():
    app = QApplication([])
    temp = AnimButton()

    baseP = os.curdir + "/walkFrames"
    frames = os.listdir(baseP)

    # convertedFrames = temp._convertFrame(baseP, frames)

    temp.setFrames(baseP, frames)
    # temp.setDownFrames(baseP, frames)
    # temp.setUpFrames(baseP, reversed(frames))

    temp.show()
    app.exec_()


main()

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QCursor
import pyautogui
from PIL import ImageGrab
import numpy as np
import cv2
import sys

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None
        self.loc = None
        self.begin = QPoint()
        self.end = QPoint()
        screenWidth, screenHeight = pyautogui.size()
        self.lightBlue = QColor(128, 128, 255, 128)

        self.setGeometry(0, 0, screenWidth, screenHeight)
        self.setWindowTitle(' ')
        self.setWindowOpacity(0.3)
        QApplication.setOverrideCursor(
            QCursor(Qt.CrossCursor)
        )
        self.setWindowFlags(Qt.FramelessWindowHint)
        print('Capture the screen...')
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(self.lightBlue)
        rect = QRect(self.begin, self.end)
        painter.drawRect(rect)

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        # ScreenshotMenu.Menu(img, 1, (x1, y1, x2, y2))
        self.image = img
        self.loc = (x1, y1, x2, y2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()

    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
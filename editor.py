from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QAction, QPushButton, QMenu, QInputDialog
from PyQt5.QtCore import QPoint, Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QPixmap, QImage, QPen
import sys
from PIL.ImageQt import ImageQt
from PIL import ImageGrab
import numpy as np
import cv2
from os.path import basename, exists
from os import makedirs

class Menu(QMainWindow):
    MARKER = 1
    PEN = 2
    COLORS = ['Red',]
    def __init__(self, img=None, snipNumber=None, startPosition=(100,100,200,150)):
        super().__init__()
        self.drawFlag = False
        self.begin = QPoint()
        self.end = QPoint()
        self.file_path = None
        self.title = str(snipNumber)
        self.cmnt = ''
        #tools
        self.tool = Menu.MARKER
        self.previousTool = self.tool

        # Save
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save')
        save_action.triggered.connect(self.save_file)

        # Exit
        exit_window = QAction('Exit', self)
        exit_window.setShortcut('Ctrl+Q')
        exit_window.setStatusTip('Exit')
        exit_window.triggered.connect(self.close)

        # Pen
        pen = QAction('Pen', self)
        pen.setShortcut('Ctrl+P')
        pen.setStatusTip('Pen')
        pen.triggered.connect(self.setPen)

        # Marker
        marker = QAction('Marker', self)
        marker.setShortcut('Ctrl+M')
        marker.setStatusTip('Marker')
        marker.triggered.connect(self.setMarker)

        # Comment
        comment = QAction('Comment', self)
        comment.setShortcut('Ctrl+D')
        comment.setStatusTip('Add Comment')
        comment.triggered.connect(self.addComment)

        # Color Picker
        brush_color_button = QPushButton("Brush Color")
        colorMenu = QMenu()
        for color in Menu.COLORS:
            colorMenu.addAction(color)
        brush_color_button.setMenu(colorMenu)
        colorMenu.triggered.connect(lambda action: change_brush_color(action.text()))

        # add to Toolbar
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(save_action)
        self.toolbar.addAction(marker)
        self.toolbar.addAction(pen)
        self.toolbar.addAction(comment)
        self.toolbar.addAction(exit_window)
        self.toolbar.addWidget(brush_color_button)

        self.setGeometry(*startPosition)

        if img is not None and snipNumber is not None:
            # qimg = ImageQt(img)       # Must revisit
            # self.image = QPixmap.fromImage(qimg)
            self.image = self.convert_img_to_qpixmap(img)
        else:
            self.image = QPixmap('background.PNG')

        self.resize(self.image.width(), self.image.height() + self.toolbar.height())
        self.show()

        def change_brush_color(new_color):
            self.brushColor = eval("Qt.{0}".format(new_color.lower()))

    # add Comment
    def addComment(self):
        comment, act = QInputDialog.getText(self, 'Comment', 'Enter the Comment')
        if(act):
            self.cmnt = str(comment)

    # Marker action
    def setMarker(self):
        self.tool = Menu.MARKER
        self.previousTool = Menu.MARKER

    # Pen action
    def setPen(self):
        self.tool = Menu.PEN
        self.previousTool = Menu.PEN

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = QRect(0, self.toolbar.height(), self.image.width(), self.image.height())
        painter.drawPixmap(rect,self.image)

        if(self.tool == Menu.PEN):
                painter = QPainter(self.image)
                painter.setPen(QPen(Qt.red, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(self.begin, self.end)
                self.begin = self.end 

        if(self.tool == Menu.MARKER):
                # painter = QPainter(self)
                # painter.setBrush(QColor(255, 255, 0, 150))
                painter.setPen(QPen(QColor(255, 0, 0, 150), 3))
                painter.drawRect(QRect(self.begin + QPoint(0, self.toolbar.height()), self.end + QPoint(0, self.toolbar.height())))


    def mousePressEvent(self,event):
        if(event.button() == Qt.LeftButton):
            self.drawFlag = True
            self.tool = self.previousTool
            self.begin = event.pos() - QPoint(0, self.toolbar.height())
            self.end = self.begin
            self.update()

    def mouseMoveEvent(self, event):
        if(event.buttons() and Qt.LeftButton and self.drawFlag):
            self.end = event.pos() - QPoint(0, self.toolbar.height())
            self.update()

    def mouseReleaseEvent(self,event):
        if(self.tool == Menu.MARKER):
            painter = QPainter(self.image)
            painter.setPen(QPen(QColor(255, 0, 0, 150), 3))
            # painter.setBrush(QColor(255, 255, 0, 170))
            painter.drawRect(QRect(self.begin, self.end))
            self.previousTool = self.tool
            self.tool = None
            self.update()
            self.begin = QPoint()
            self.end = QPoint()


        self.drawFlag = False



    def save_file(self):
        # file_path, name = QFileDialog.getSaveFileName(self, "Save file", self.title, "PNG Image file (*.png)")
        self.file_path = 'C:\\Users\\736131\\Documents\\ScreenshotAuto\\screenshot'
        if not exists(self.file_path):
            makedirs(self.file_path)
        
        self.file_path = self.file_path+'\\'+self.title+'.png'
        if self.file_path:
            self.image.save(self.file_path)
            self.title = basename(self.file_path)
            self.setWindowTitle(self.title)
            print(self.title, 'Saved')
            self.close()
        # return file_path


    @staticmethod
    def convert_img_to_qpixmap(img):
        np_img = img
        np_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        height, width, channel = np_img.shape
        bytesPerLine = 3 * width
        return QPixmap(QImage(np_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    img = ImageGrab.grab()
    mainMenu = Menu(img, 1)
    sys.exit(app.exec_())          



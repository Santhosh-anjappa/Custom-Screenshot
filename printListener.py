from PyQt5.QtWidgets import QWidget, QApplication
from pynput import keyboard
from time import time
import sys
from snipper import MyWidget
import editor
from documentMaker import Doc

COMBINATIONS = [
    {keyboard.Key.print_screen}
]
EXIT = [{keyboard.Key.ctrl, keyboard.KeyCode(char='c')},]
current = set()

shotCount = 1
def execute():
    global shotCount

    cells = doc.addRows()
    app = QApplication(sys.argv)
    window = MyWidget()
    app.exec_()
    img = window.image
    loc = window.loc

    menu = editor.Menu(img, shotCount, loc)
    app.exec_()

    imgFile = menu.file_path
    comment = menu.cmnt

    if(imgFile is not None):
        doc.addImageToCell(imgFile, cells)
        doc.save('TestDemo.docx')
    if(comment):
        doc.addComment(comment,cells)
        doc.save('TestDemo.docx')

    shotCount += 1
    # app.aboutToQuit.connect(app.deleteLater)

def on_press(key):
    if any([key in COMBO for COMBO in EXIT]):
        sys.exit(0)

    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()


def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)

doc = Doc()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Ready........")
    listener.join()
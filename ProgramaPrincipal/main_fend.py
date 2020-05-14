from PyQt5.QtWidgets import QApplication
from BackEnd.BackEnd import BackEnd
from FrontEnd.src.MainWindow import MyMainWindow
import os

from BackEnd.path import origin as path

if __name__ == "__main__":
    app = QApplication([])
    back = BackEnd()
    widget = MyMainWindow(backend=back)
    widget.show()
    app.exec()
    dir_name = path + "BackEnd/Tracks"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".npy"):
            os.remove(os.path.join(dir_name, item))

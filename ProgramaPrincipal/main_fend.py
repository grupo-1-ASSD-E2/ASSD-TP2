from PyQt5.QtWidgets import QApplication
from BackEnd.BackEnd import BackEnd
from FrontEnd.src.MainWindow import MyMainWindow
from BackEnd.AudioEfects.convolutioner import Convolutioner
import os

from BackEnd.path import origin as path

if __name__ == "__main__":
    app = QApplication([])
    back = BackEnd()
    media_player = Convolutioner()
    widget = MyMainWindow(backend=back, convolutioner=media_player)
    widget.show()
    app.exec()
    dir_name = path + "BackEnd/Tracks"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".npy"):
            os.remove(os.path.join(dir_name, item))

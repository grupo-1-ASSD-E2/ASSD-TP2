from PyQt5.QtWidgets import QApplication
from BackEnd.BackEnd import BackEnd
from FrontEnd.src.MainWindow import MyMainWindow


if __name__ == "__main__":
    app = QApplication([])
    back = BackEnd()
    widget = MyMainWindow(backend=back)
    widget.show()
    app.exec()

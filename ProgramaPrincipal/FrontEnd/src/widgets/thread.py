from PyQt5.QtCore import QThread, pyqtSignal


class Thread(QThread):
    track_ready = pyqtSignal(int)

    def __init__(self, function):
        QThread.__init__(self)
        self.fun = function

    def __del__(self):
        self.wait()

    def run(self) -> None:
        self.fun()


# PyQt5 modules
from PyQt5.QtWidgets import QWidget, QApplication

# Project modules
from FrontEnd.src.ui.botonera import Ui_MediaObject


class MediaButtonsWidget(QWidget, Ui_MediaObject):

    def __init__(self, parent=None):
        super(MediaButtonsWidget, self).__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication([])
    widget = MediaButtonsWidget()
    widget.show()
    app.exec()

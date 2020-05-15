# PyQt5 modules
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import pyqtSignal

# Project modules
from FrontEnd.src.ui.note import Ui_Form


class NoteWidget(QWidget, Ui_Form):

    delete = pyqtSignal()

    def __init__(self, freq, instrument, vol, init, long, parent=None):
        super(NoteWidget, self).__init__(parent)
        self.setupUi(self)
        self._freq = freq
        self._instrument = instrument
        self._vol = vol
        self._init = init
        self._long = long

        self.freq.setText('Frecuencia: '+str(freq))
        self.inst.setText(instrument)
        self.col.setText('Velocity: '+str(vol))
        self.init.setText('Inicio: '+str(init)+' s')
        self.long_2.setText('Largo: '+str(long)+' s')
        self.pushButton.clicked.connect(lambda : self.delete.emit())

    def get_data(self):
        return self._init, self._long, self._vol, self._instrument, self._freq


if __name__ == "__main__":
    app = QApplication([])
    widget = NoteWidget()
    widget.show()
    app.exec()

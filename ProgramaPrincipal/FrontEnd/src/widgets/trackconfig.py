# PyQt5 modules
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import pyqtSignal

# Project modules
from FrontEnd.src.ui.midi_instrument import Ui_track


class TrackConfigWidget(QWidget, Ui_track):

    clicked = pyqtSignal()
    mute_signal = pyqtSignal(bool, int)

    def __init__(self, parent=None, name=None, instruments=None):
        super(TrackConfigWidget, self).__init__(parent)
        self.setupUi(self)
        if name is not None:
            self.name.setText('Track ' + name)
        self.track_num = name
        if instruments is not None:
            self.instrument_getter = instruments
        self.instrument.clicked.connect(self.get_instrument)
        self.widget.mouseReleaseEvent = lambda event: self.clicked.emit()
        self.mute.clicked.connect(self.mute_state)


    """
    def click(self):
        if self.preview.isChecked():
            self.setStyleSheet('QWidget { border-style: solid; background-color: rgb(24, 180, 24); border-radius: 5px;}')
        else:
            self.setStyleSheet('QWidget { border-style: solid; background-color: rgb(81, 76, 149); border-radius: 5px;}')
    """
    def mute_state(self):
        """ If muted, state = True """
        state = self.mute.isChecked()
        self.mute_signal.emit(state, self.track_num)

    def get_data(self):
        volume = 0 if self.mute.isChecked() else self.volume.value()
        instrument = self.instrument.toolTip()
        return volume, instrument

    def set_instrument(self, instrument_data):
        """ instrument data should be a tuple (instrument, image) """
        self.instrument.setToolTip(instrument_data[0])
        self.instrument.setStyleSheet("image: url(:/" + instrument_data[1] + ");")

    def get_instrument(self):
        self.instrument_getter.show()
        self.instrument_getter.set_receiver(self)

    def get_track_number(self):
        return self.track_num


if __name__ == "__main__":
    app = QApplication([])
    widget = TrackConfigWidget()
    widget.show()
    app.exec()

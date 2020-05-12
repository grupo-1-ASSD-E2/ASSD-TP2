# Python modules
import functools

# PyQt5 modules
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QSizePolicy, QGridLayout

# Project modules
from FrontEnd.src.ui.instruments import Ui_Instruments
from FrontEnd.src.widgets.trackconfig import TrackConfigWidget
from BackEnd.Instruments import Instruments


class InstrumentsPopUp(QWidget, Ui_Instruments):

    def __init__(self, parent=None):
        super(InstrumentsPopUp, self).__init__(parent)
        self.setupUi(self)

        self.base_button_4.hide()
        self.receiver = None

        layout = self.button_collector.layout()

        layout.setColumnStretch(1, 5)
        layout.setColumnStretch(2, 5)

        buttons = []
        for i in Instruments:
            aux = QPushButton()
            aux.setFixedWidth(50)
            aux.setFixedHeight(50)
            aux.setToolTip(i.value[0])
            aux.setStyleSheet("image: url(:/"+i.value[1]+");")
            aux.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            aux.clicked.connect(functools.partial(self.instrument_selected, i))
            buttons.append(aux)

        for i in range(0, len(buttons)):
            layout.addWidget(buttons[i], int(i/4), int(i % 4))

    def set_receiver(self, receiver: TrackConfigWidget):
        self.receiver = receiver

    def instrument_selected(self, instrument):
        if self.receiver is not None:
            self.receiver.set_instrument(instrument.value)
            self.receiver = None

        self.hide()


if __name__ == "__main__":
    app = QApplication([])
    widget = InstrumentsPopUp()
    widget.show()
    app.exec()

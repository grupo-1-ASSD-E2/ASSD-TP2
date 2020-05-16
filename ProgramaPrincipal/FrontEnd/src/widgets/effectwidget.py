# PyQt5 modules
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import pyqtSignal

# Project modules
from FrontEnd.src.ui.effect_property import Ui_e_prop


class EffectPropertyWidget(QWidget, Ui_e_prop):

    value_change = pyqtSignal((str, float), name='valueChange')

    def __init__(self, parent=None, property: str = '', limits=(0, 100), default_value=50):
        super(EffectPropertyWidget, self).__init__(parent)
        self.setupUi(self)
        self.me = property

        self.Prop.setText(property)

        self.offset = limits[0]
        self.k = (limits[1]-limits[0])/100.0
        self.preset.valueChanged.connect(self.update_value)
        self.preset.setSliderPosition(int(self.k*(default_value+self.offset)))
        self.value.setNum(default_value)

    def update_value(self, new_value):
        nuevo = self.k*new_value+self.offset
        self.value.setNum(nuevo)
        self.value_change.emit(self.me, nuevo)


if __name__ == "__main__":
    app = QApplication([])
    widget = EffectPropertyWidget()
    widget.show()
    app.exec()

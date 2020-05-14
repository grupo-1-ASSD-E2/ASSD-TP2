# PyQt5 modules
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import pyqtSignal

# Project modules
from FrontEnd.src.ui.used_tack import Ui_worked_track
from BackEnd.AudioEfects.BaseAudioEffect.BaseEffect import Effect
import numpy as np


class EditedTrackWidget(QWidget, Ui_worked_track):

    update_effect = pyqtSignal()  # Tell the program to update
    clicked = pyqtSignal(int)

    def __init__(self, parent=None, properties_layout=None, track_number=-1):
        super(EditedTrackWidget, self).__init__(parent)
        self.setupUi(self)
        self.prop_layout = properties_layout
        self.widget.mouseReleaseEvent = lambda event: self.clicked.emit(self.track_num)

        """ Efect """
        self.effect_instance = None
        self.properties = []

        """ Track things """
        self.track_num = track_number
        self.track.setText("Track N° " + str(track_number))

        """ Connect with mute button """
        self.is_muted = False
        self.mute.clicked.connect(self.mute_click)

    def go_backstage(self):
        for each in self.properties:
            each.hide()

    def close_all(self):
        for old in self.properties:
            #self.prop_layout.removeWidget(old)
            old.close()

    def show_properties(self):
        for prop in self.properties:
            prop.show()

    def get_properties(self):
        return self.properties

    def set_effect(self, effect_instance, new_properties):

        """ Keep new effect instance """
        self.effect_instance = effect_instance
        self.effect.setText(self.effect_instance.name)

        """ Close old properties widgets and save new ones """
        for old in self.properties:
            #self.prop_layout.removeWidget(old)
            old.close()
        self.properties = new_properties
        for new_prop in self.properties:
            new_prop.value_change.connect(self.update_callback)

        """ After changing instance renew the callback for convolutioner """
        self.update_effect.emit()

    def update_callback(self, prop2change, new_value):
        self.effect_instance.change_param(prop2change, new_value)

    def reset(self):
        self.effect_instance.clear()

    def mute_click(self):
        self.is_muted = not self.is_muted
        self.update_effect.emit()

    def get_callback(self):
        if self.is_muted:
            return self.muted_callback
        else:
            return self.effect_instance.compute

    @staticmethod
    def muted_callback(sample):
        out = np.array([np.zeros(len(sample))])
        return (out, out)


if __name__ == "__main__":
    app = QApplication([])
    widget = EditedTrackWidget()
    widget.show()
    app.exec()

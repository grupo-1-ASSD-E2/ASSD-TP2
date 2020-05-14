# Python modules
import functools

# PyQt5 modules
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

# Project modules
from FrontEnd.src.ui.main_window import Ui_AudioTool
from FrontEnd.src.widgets.trackconfig import TrackConfigWidget
from FrontEnd.src.widgets.instruments import InstrumentsPopUp
from FrontEnd.src.widgets.effectwidget import EffectPropertyWidget
from BackEnd.BackEnd import BackEnd
from BackEnd.Effects import Effects

"""
Espectrogram

"""


class MyMainWindow(QMainWindow, Ui_AudioTool):

    def __init__(self, parent=None, backend=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.working = False
        self.audio_available = False
        self.old_preview = None

        """ Hide samples """
        self.track_0.hide()
        self.effect_0.hide()

        """ Set up sintesis enviroment """
        self.track_manager = []
        self.instrument_panel = InstrumentsPopUp()
        self.select_file.clicked.connect(self.open_midi)
        self.sintetizar.clicked.connect(self.create_tracks)
        self.backend = backend

        """ Media player buttons """
        self.media_buttons_widget.play.clicked.connect(self.play)
        self.media_buttons_widget.stop.clicked.connect(self.stop)

        """ Effects enviroment """
        self.old_effect_prop = []
        self.current_effects_properties = []
        self.to_track.setDisabled(True)
        self.to_song.setDisabled(True)
        #self.choose_effect.setDisabled(True)
        self.choose_effect.addItem('')
        self.effects = []
        for i in Effects:
            self.effects.append(i.value)
            self.choose_effect.addItem(i.value[0])
        self.choose_effect.currentIndexChanged.connect(self.renew_effect)
        self.to_song.clicked.connect(self.effect_to_song)
        self.to_track.clicked.connect(self.effect_to_track)
        #self.showFullScreen()

    def effect_to_song(self, selected):
        pass

    def effect_to_track(self, selected):
        pass

    def renew_effect(self, index):
        layout = self.effect_container.layout()
        size = self.effect_0.sizePolicy()
        for old in self.old_effect_prop:
            layout.removeWidget(old)
            old.close()

        self.old_effect_prop = []
        if index > 0:
            efecto = self.effects[index-1]
            propiedades = efecto[1]
            for prop, valor in propiedades.items():
                my_item = EffectPropertyWidget(self, prop, valor[0][1], valor[1])
                #my_item.setSizePolicy(size)
                layout.addWidget(my_item)
                self.old_effect_prop.append(my_item)

    def open_midi(self):
        layout = self.track_setter.layout()
        """ Clear old tracks """
        for old_track in self.track_manager:
            layout.removeWidget(old_track)

        self.track_manager = []  # Clear previous tracks

        """ Go to find new """
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Midi (*.mid)')
        """ If no file is selected quit """
        if filename == '':
            return

        name = filename.split('/')[-1]
        self.midi_name.setText(name)
        self.backend.load_midi_file(filename)
        tracks = self.backend.get_track_list()

        for i in range(0, len(tracks)):
            aux_track = TrackConfigWidget(self, str(i+1), self.instrument_panel)
            aux_track.preview.clicked.connect(functools.partial(self.preview_adjust, i))
            self.track_manager.append(aux_track)
            layout.addWidget(self.track_manager[i])
            # i += 1

    def create_tracks(self):
        if not self.working:
            self.working = True
            for i in range(0, len(self.track_manager)):
                volume, instrument = self.track_manager[i].get_data()
                self.backend.assign_instrument_to_track(i, instrument, volume/100.0)
                if volume == 0 or instrument == '':
                    pass
                    #self.backend.toggle_track(i)

            self.backend.synthesize_song()
            self.working = False

    def play(self):
        if self.media_buttons_widget.stop.isChecked():
            self.media_buttons_widget.stop.toggle()
        if self.old_preview is not None:
            pass  # should only play 1 track
        else:
            pass
            self.backend.play_song()

    def stop(self):
        if self.media_buttons_widget.play.isChecked():
            self.media_buttons_widget.play.toggle()
        #self.backend.stop_reproduction()

    def preview_adjust(self, track_number):
        if self.old_preview is not None:
            if self.old_preview != track_number:
                """ Clear previous select """
                self.track_manager[self.old_preview].setStyleSheet(
                    'QWidget { border-style: solid; background-color: rgb(81, 76, 149); border-radius: 5px;}')
                self.track_manager[self.old_preview].preview.toggle()

                """ Mark new track"""
                self.track_manager[track_number].setStyleSheet(
                    'QWidget { border-style: solid; background-color: rgb(31, 172, 102); border-radius: 5px;}')
                self.old_preview = track_number
            else:
                """ Unselect track """
                self.track_manager[self.old_preview].setStyleSheet(
                    'QWidget { border-style: solid; background-color: rgb(81, 76, 149); border-radius: 5px;}')
                self.old_preview = None
        else:
            self.track_manager[track_number].setStyleSheet(
                'QWidget { border-style: solid; background-color: rgb(31, 172, 102); border-radius: 5px;}')
            self.old_preview = track_number


if __name__ == "__main__":
    app = QApplication([])
    widget = MyMainWindow()
    widget.show()
    app.exec()

# Python modules
import functools

# PyQt5 modules
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

# Project modules
from FrontEnd.src.ui.main_window import Ui_AudioTool
from FrontEnd.src.widgets.trackconfig import TrackConfigWidget
from FrontEnd.src.widgets.instruments import InstrumentsPopUp
from BackEnd.BackEnd import BackEnd
from BackEnd.Track import Track


class MyMainWindow(QMainWindow, Ui_AudioTool):

    def __init__(self, parent=None, backend: BackEnd = None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.working = False
        self.old_preview = None
        self.track_0.hide()
        self.track_manager = []
        self.instrument_panel = InstrumentsPopUp()
        self.select_file.clicked.connect(self.open_midi)
        self.sintetizar.clicked.connect(self.create_tracks)
        self.backend = backend
        self.media_buttons_widget.pause.clicked.connect(self.pause)
        self.media_buttons_widget.play.clicked.connect(self.play)
        self.media_buttons_widget.stop.clicked.connect(self.stop)

    def open_midi(self):
        self.track_manager = []  # Clear previous tracks

        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Midi (*.mid)')
        name = filename.split('/')[-1]
        self.midi_name.setText(name)
        self.backend.load_midi_file(filename)
        tracks = self.backend.get_track_list()
        layout = self.track_setter.layout()
        print(len(tracks))
        for i in range(0, len(tracks)):
            aux_track = TrackConfigWidget(self, str(i+1), self.instrument_panel)
            aux_track.preview.clicked.connect(functools.partial(self.preview_adjust, i))
            self.track_manager.append(aux_track)
            layout.addWidget(self.track_manager[i])
            i += 1

    def create_tracks(self):
        if not self.working:
            self.working = True
            for i in range(0, len(self.track_manager)):
                volume, instrument = self.track_manager[i].get_data()
                self.backend.assign_instrument_to_track(i, instrument, volume/100.0)
                if volume == 0 or instrument == '':
                    self.backend.toggle_track(i)

            self.backend.synthesize_song()
            self.backend.play_song()
            self.working = False

    def play(self):
        if self.media_buttons_widget.pause.isChecked():
            self.media_buttons_widget.pause.toggle()
        if self.media_buttons_widget.stop.isChecked():
            self.media_buttons_widget.stop.toggle()

    def pause(self):
        if self.media_buttons_widget.play.isChecked():
            self.media_buttons_widget.play.toggle()
        if self.media_buttons_widget.stop.isChecked():
            self.media_buttons_widget.stop.toggle()
        pass

    def stop(self):
        if self.media_buttons_widget.pause.isChecked():
            self.media_buttons_widget.pause.toggle()
        if self.media_buttons_widget.play.isChecked():
            self.media_buttons_widget.play.toggle()
        pass

    def preview_adjust(self, track_number):
        if self.old_preview is not None:
            if self.old_preview != track_number:
                """ Clear previous select """
                self.track_manager[self.old_preview].setStyleSheet(
                    'QWidget { border-style: solid; background-color: rgb(81, 76, 149); border-radius: 5px;}')
                self.track_manager[self.old_preview].preview.toggle()

                """ Mark new track"""
                self.track_manager[track_number].setStyleSheet(
                    'QWidget { border-style: solid; background-color: rgb(81, 76, 149); border-radius: 5px;}')
                self.old_preview = track_number
            else:
                """ Unselect track """
                self.track_manager[self.old_preview].setStyleSheet(
                    'QWidget { border-style: solid; background-color: rgb(81, 76, 149); border-radius: 5px;}')
                self.old_preview = None
        else:
            self.track_manager[track_number].setStyleSheet(
                'QWidget { border-style: solid; background-color: rgb(81, 76, 149); border-radius: 5px;}')
            self.old_preview = track_number


if __name__ == "__main__":
    app = QApplication([])
    back = BackEnd()
    widget = MyMainWindow(backend=back)
    widget.show()
    app.exec()

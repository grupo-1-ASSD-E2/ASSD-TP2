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
        i = 0
        layout = self.track_setter.layout()
        print(len(tracks))
        for each in tracks:
            self.track_manager.append(TrackConfigWidget(self, str(i+1), self.instrument_panel))
            layout.addWidget(self.track_manager[i])
            i += 1

    def create_tracks(self):
        for i in range(0, len(self.track_manager)):
            volume, instrument = self.track_manager[i].get_data()
            self.backend.assign_instrument_to_track(i, instrument)
            if volume == 0:
                self.backend.toggle_track(i)

        self.backend.synthesize_song()
        self.backend.play_song()

    def play(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

if __name__ == "__main__":
    app = QApplication([])
    back = BackEnd()
    widget = MyMainWindow(backend=back)
    widget.show()
    app.exec()

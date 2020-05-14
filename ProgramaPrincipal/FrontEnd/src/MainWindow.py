# Python modules
import functools
import numpy as np
from multiprocessing import Pool

# PyQt5 modules
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import QTime
from PyQt5.QtCore import QTimer

# Project modules
from FrontEnd.src.ui.main_window import Ui_AudioTool
from FrontEnd.src.widgets.trackconfig import TrackConfigWidget
from FrontEnd.src.widgets.instruments import InstrumentsPopUp
from FrontEnd.src.widgets.effectwidget import EffectPropertyWidget
from FrontEnd.src.widgets.effectedtrack import EditedTrackWidget
from BackEnd.BackEnd import BackEnd
from BackEnd.Effects import Effects
from BackEnd.GUI_resources.spectrogram_plotter import Spectrogrammer, PyQtPlotter
from BackEnd.path import origin as path
"""
Reminders:
            + Espectrogram
            + Convolutioner

"""


class MyMainWindow(QMainWindow, Ui_AudioTool):

    def __init__(self, parent=None, backend=None, convolutioner=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.backend = backend
        self.media_player = convolutioner
        self.media_player.custom_processing_callback(self.audio_callback)

        self.working = False
        self.audio_available = False
        self.old_preview = None
        self.synthesis_stage = True

        """ Hide samples """
        self.track_0.hide()
        self.effect_0.hide()

        """ Set up sintesis enviroment """
        self.track_manager = []
        self.instrument_panel = InstrumentsPopUp()
        self.select_file.clicked.connect(self.open_midi)
        self.sintetizar.clicked.connect(self.create_tracks)
        self.sintetizar.setDisabled(True)  # No synthesis whitout midi
        self.available_to_play = []

        """ Media player buttons """
        self.media_buttons_widget.play.clicked.connect(self.play)
        self.media_buttons_widget.stop.clicked.connect(self.stop)

        """ Effects enviroment """
        self.working_tracks = []  # To store on working EditedTrackWidget
        self.current_track = -1
        self.old_effect_prop = []
        self.current_effects_properties = []
        self.choose_effect.addItem('')
        self.effects = []
        for i in Effects:
            self.effects.append(i.value)
            self.choose_effect.addItem(i.value[0])
        self.choose_effect.currentIndexChanged.connect(self.renew_effect)
        self.to_song.clicked.connect(self.effect_to_song)
        self.to_track.clicked.connect(self.effect_to_track)
        self.discard_effect.clicked.connect(self.clean_current_effect)

        self.disable_effect_enviroment()

        """ Reproduction thing """
        self.all_tracks = []
        self.all_callbacks = []

        """ Timer things """
        self.inner_timer = QTimer()
        self.inner_timer.timeout.connect(self.count_down_callback)
        self.song_time = QTime()

        """ Spectrogram things """
        self.spectrogrammer = Spectrogrammer()
        self.plotter = PyQtPlotter()
        self.plot_work.clicked.connect(self.sepectro_plot)

    def sepectro_plot(self):
        source = self.plot_track.currentText()
        data = []
        if source == '':
            """ Incomplete """
            return
        elif source == 'Plain Song':
            data = np.sum(self.all_tracks, axis=0)
        elif source == 'Edited Song':
            data = self.media_player.output_array.copy()
        else:
            track_num = int(source.split()[-1])
            useful_index = self.available_to_play.index(track_num-1)
            data = self.all_tracks[useful_index]
        """ Ya tenemos los datos ahora hay que cortar el tramo de tiempo que se quiera """

        init = 44100*self.plot_time.time().minute()*60+self.plot_time.time().second()
        fin = init+(self.plot_long.value()*44100)

        song = data[init:fin]
        time_array = np.arange(0, song.size/44100.0, 1/44100, dtype=song.dtype)
        self.spectrogrammer.compute_audio_array(time_array, song)
        self.spectrogrammer.calculate_FFTs()

        mag = self.spectrogrammer.get_FFTs_magnitude()
        time = self.spectrogrammer.get_resampled_time_array()
        freq = self.spectrogrammer.get_FFTs_freq()

        util_canvas = self.plotter.spectrogram(time, freq, mag)



        """
        if self.plot_space.count() > 2:
        
        try:
            old = self.plot_space
            self.plot_space.layout().removeWidget(old)
        except Exception:
            pass
        """

        self.plot_space.addWidget(util_canvas)

        #toolbar = NavigationToolbar(self.plotters[0].canvas, self)
        #if self.toolbar_1.count() > 2:
        #    # Cleaning stacked widget
        #    self.toolbar_1.removeWidget(self.filter_data.currentWidget())
        #self.toolbar_1.setCurrentIndex(self.toolbar_1.addWidget(toolbar))


    def count_down_callback(self):
        if self.media_player.processing():
            self.song_time = self.song_time.addSecs(-1)
            self.count_down.setText(self.song_time.toString("m:ss"))
        else:
            self.plot_track.addItem('Edited Song')
            self.count_down.setText('00:00')
            self.media_player.terminate_processing()
            self.inner_timer.stop()
            self.media_buttons_widget.play.toggle()
            for i in self.working_tracks:
                i.reset()

    def disable_effect_enviroment(self):
        self.plot_track.clear()

        self.working = False
        self.audio_available = False
        self.old_preview = None
        self.synthesis_stage = True

        self.media_buttons_widget.play.setDisabled(True)
        self.media_buttons_widget.stop.setDisabled(True)

        self.to_track.hide()
        self.to_song.hide()
        self.choose_effect.setDisabled(True)
        self.discard_effect.hide()
        self.work_track.setText('')

        for tracks in self.track_manager:  # Closing old midi tracks
            tracks.close()

        for track_edits in self.working_tracks:
            track_edits.close_all()  # Clean up old work / be careful with convolutioner!!!

    def enable_effects(self):
        self.synthesis_stage = False
        self.media_buttons_widget.play.setDisabled(False)
        self.media_buttons_widget.stop.setDisabled(False)
        #self.to_track.show()
        #self.to_song.show()

    def clean_current_effect(self):
        """ First change the callback to use, then reapear and to finish clean everything """
        track = self.working_tracks[self.current_track].track_num - 1
        useful_index = self.available_to_play.index(track)
        if useful_index < 0:
            print('Fatal ERROR')
        self.all_callbacks[useful_index] = self.nothing  # Setting new callback
        self.track_manager[track].show()  # Reapear in tracks
        self.work_track.setText("Track ...")
        self.choose_effect.setDisabled(True)

        self.working_tracks[self.current_track].close_all()
        self.working_tracks[self.current_track].close()
        self.working_tracks.pop(self.current_track)
        self.current_track = -1

    def get_back_effect(self, track_number):
        who = -1
        j = 0
        for i in self.working_tracks:
            if i.track_num == track_number:
                who = j
                break
            else:
                j += 1
        if who == self.current_track:
            """ Nothing to do """
            return

        if self.current_track >= 0:
            self.working_tracks[self.current_track].go_backstage()
            self.choose_effect.setCurrentIndex(0)

        self.choose_effect.setDisabled(False)
        self.work_track.setText("Track " + str(track_number))
        self.discard_effect.show()

        self.current_track = who
        self.working_tracks[who].show_properties()

    def audio_callback(self, sample):
        out = np.array(list(map(lambda audio, fun: fun(audio), sample, self.all_callbacks)))
        return out[:, 0], out[:, 1]

    def effect_to_song(self):
        print('hola')

    def effect_to_track(self, selected):
        pass

    def select_track(self, index):
        if not (not self.synthesis_stage and index in self.available_to_play):
            """ If synthesis is not ready, effects are not possible """
            return

        if self.current_track >= 0:
            self.working_tracks[self.current_track].go_backstage()
            self.choose_effect.setCurrentIndex(0)

        self.track_manager[index].hide()
        self.choose_effect.setDisabled(False)
        self.work_track.setText("Track "+str(index+1))
        self.discard_effect.show()

        temp = EditedTrackWidget(self, self.effect_container.layout(), index+1)
        self.working_tracks.append(temp)
        self.working_effects.layout().addWidget(temp)
        self.current_track = self.working_tracks.index(temp)
        temp.update_effect.connect(self.audio_procesing)
        temp.clicked.connect(self.get_back_effect)

    def audio_procesing(self):
        track = self.working_tracks[self.current_track].track_num-1
        useful_index = self.available_to_play.index(track)
        if useful_index < 0:
            print('Fatal ERROR')
        self.all_callbacks[useful_index] = self.working_tracks[self.current_track].get_callback()

    def tracks_audio_prcesing(self, state: bool, index: int):
        index = index-1
        useful_index = self.available_to_play.index(index)
        if useful_index >= 0:
            """ Available ones """
            if state:
                self.all_callbacks[useful_index] = self.mute
            else:
                self.all_callbacks[useful_index] = self.nothing

    def renew_effect(self, index):
        layout = self.effect_container.layout()

        if index > 0:
            self.old_effect_prop = []

            efecto = self.effects[index-1]
            propiedades = efecto[1]
            for prop, valor in propiedades.items():
                my_item = EffectPropertyWidget(self, prop, valor[0][1], valor[1])
                layout.addWidget(my_item)
                self.old_effect_prop.append(my_item)
            self.working_tracks[self.current_track].set_effect(efecto[2](), self.old_effect_prop)

    def open_midi(self):
        layout = self.track_setter.layout()

        """ Go to find new """
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Midi (*.mid)')
        """ If no file is selected quit """
        if filename == '':
            return

        """ Clear previous things"""
        self.disable_effect_enviroment()

        name = filename.split('/')[-1]
        self.midi_name.setText(name)
        self.backend.load_midi_file(filename)
        tracks = self.backend.get_track_list()

        for i in range(0, len(tracks)):
            aux_track = TrackConfigWidget(self, str(i+1), self.instrument_panel)
            aux_track.clicked.connect(functools.partial(self.select_track, i))
            """ Aca deberia agarrar el doble ckick !!!!"""
            self.track_manager.append(aux_track)
            layout.addWidget(self.track_manager[i])
            # i += 1

        self.sintetizar.setDisabled(False)

    def create_tracks(self):

        """ working is a bool to avoid  conflicts while synthesizing """
        if not self.working:
            """ May be good looking to start a timer and do something meanwhile.. """
            self.working = True
            absents = []
            all_num = []
            for i in range(0, len(self.track_manager)):
                all_num.append(i)
                volume, instrument = self.track_manager[i].get_data()
                self.backend.assign_instrument_to_track(i, instrument, volume/100.0)
                if volume == 0 or instrument == '':
                    absents.append(i)
                    self.backend.toggle_track(i)

            self.available_to_play = list(set(all_num).difference(set(absents)))
            for a in self.available_to_play:
                self.track_manager[a].setStyleSheet(
                    'QWidget { border-style: solid; background-color: rgb(31, 172, 102); border-radius: 5px;}')
            for a in absents:  # This may be useful in future
                self.track_manager[a].setStyleSheet(
                    'QWidget { border-style: solid; background-color: rgbrgb(81, 76, 149); border-radius: 5px;}')
            self.backend.synthesize_song()
            self.enable_effects()
            self.plot_track.addItem('Plain Song')
            self.plot_track.addItems(['Track '+str(i+1) for i in self.available_to_play])
            self.working = False
            all_tracks = []
            """ Load tracks """
            for i in range(0, len(self.available_to_play)):
                song = np.load(path + 'BackEnd/Tracks/' + 'track' + str(i) + '.npy')
                all_tracks.append(song)
                self.all_callbacks.append(self.nothing)  # Adding functions with all ones
            if self.media_player is not None:
                """ Send input to convolutioner """
                self.media_player.update_input(np.array(all_tracks), np.dtype('float32'))

            self.all_tracks = all_tracks.copy()
            """ Set timer """
            song_len = len(all_tracks[0])
            song_len = np.ceil(song_len/44100.0)
            self.song_time.setHMS(0, int(song_len/60.0), int(song_len % 60))
            self.count_down.setText(self.song_time.toString("m:ss"))

    def play(self):
        if self.media_buttons_widget.stop.isChecked():
            self.media_buttons_widget.stop.toggle()

        self.media_player.start_non_blocking_processing()
        self.inner_timer.start(1000)

    def stop(self):
        if self.media_buttons_widget.play.isChecked():
            self.media_buttons_widget.play.toggle()

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

    @staticmethod
    def nothing(sample):
        """ All deltas response, for no effect output """
        return (sample, sample)

    @staticmethod
    def mute(sample):
        """ All deltas response, for no effect output """
        out = np.array([np.zeros(len(sample))])
        return (out, out)


if __name__ == "__main__":
    app = QApplication([])
    backend = BackEnd()
    widget = MyMainWindow(backend=backend)
    widget.show()
    app.exec()
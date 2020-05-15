# Python modules
import functools
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavegationToolBar
from scipy.io.wavfile import write

# PyQt5 modules
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import QTime, QTimer

# Project modules
from FrontEnd.src.ui.main_window import Ui_AudioTool
from FrontEnd.src.widgets.trackconfig import TrackConfigWidget
from FrontEnd.src.widgets.instruments import InstrumentsPopUp
from FrontEnd.src.widgets.effectwidget import EffectPropertyWidget
from FrontEnd.src.widgets.effectedtrack import EditedTrackWidget
from FrontEnd.src.widgets.notewidget import NoteWidget
from FrontEnd.src.widgets.thread import Thread
from FrontEnd.src.note import note
from BackEnd.BackEnd import BackEnd
from BackEnd.Effects import Effects
from BackEnd.Instruments import Instruments
from BackEnd.GUI_resources.spectrogram_plotter import Spectrogrammer, PyQtPlotter
from BackEnd.path import origin as path
from scipy import signal


class MyMainWindow(QMainWindow, Ui_AudioTool):

    def __init__(self, parent=None, backend=None, convolutioner=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.backend = backend

        self.backend.track_done.connect(self.progress_count)
        self.media_player = convolutioner
        self.media_player.custom_processing_callback(self.audio_callback)

        self.working = False
        self.audio_available = False
        self.playing = False
        self.old_preview = None
        self.synthesis_stage = True

        """ Hide samples """
        self.progress_bar.hide()
        self.track_0.hide()
        self.effect_0.hide()
        self.root = ''
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
        self.plot_work.clicked.connect(self.sepectro_plot)
        self.prev_plot = None
        self.prev_nav = None

        """ Notes """
        for i in Instruments:
            self.note_instrument.addItem(i.value[0])
        self.note_add.clicked.connect(self.add_note)
        self.note_play.clicked.connect(self.play_notes)
        self.all_notes = []

        self.save.clicked.connect(self.save_wav)

    def save_wav(self):
        to_save = None
        if self.audio_available:
            to_save = self.media_player.output_array.copy()
        else:
            to_save = np.sum(self.all_tracks, axis=0)

        file = self.root+'.wav'
        write(file, 44100, np.int16(to_save * 32767))

    def play_notes(self):
        notas = []
        for i in self.all_notes:
            i, l, v, ins, f = i.get_data()
            notas.append(note(i, l, v, ins, f))

        self.backend.create_chord(notas)

    def add_note(self):
        init = self.note_time.value()
        long = self.note_duration.value()
        velocity = self.note_volume.value()
        instrument = self.note_instrument.currentText()
        freq = self.note_freq.value()
        note = NoteWidget(freq, instrument, velocity, init, long, self)
        note.delete.connect(functools.partial(self.remove_note, note))
        self.all_notes.append(note)
        self.note_area.layout().addWidget(note)

    def remove_note(self, note: NoteWidget):
        self.all_notes.remove(note)
        note.close()

    def sepectro_plot(self):
        source = self.plot_track.currentText()
        data = []
        if source == '':
            """ Incomplete """
            return
        elif source == 'Plain Song':
            data = np.sum(self.all_tracks, axis=0)
        elif source == 'Edited Song':
            data = np.sum(self.media_player.output_array.copy(), axis=0)
        else:
            track_num = int(source.split()[-1])
            useful_index = self.available_to_play.index(track_num-1)
            data = self.all_tracks[useful_index]
        """ Ya tenemos los datos ahora hay que cortar el tramo de tiempo que se quiera """

        title = source + ' init: ' + str(self.plot_time.time().minute()) + ':' + str(self.plot_time.time().second()) + \
                ' + ' + str(self.plot_long.value()) + 's'
        init = 44100*self.plot_time.time().minute()*60+self.plot_time.time().second()
        fin = init+(self.plot_long.value()*44100)

        song = data[init:fin]
        time_array = np.arange(init, init+song.size/44100.0, 1/44100.0, dtype=song.dtype)
        self.spectrogrammer.compute_audio_array(time_array, song)
        self.spectrogrammer.calculate_FFTs()

        mag = self.spectrogrammer.get_FFTs_magnitude()
        time = self.spectrogrammer.get_resampled_time_array()
        freq = self.spectrogrammer.get_FFTs_freq()

        plotter = PyQtPlotter()
        plotter.spectrogram(time, freq, mag, title, f_bottom=20, f_top=20000)
        util_canvas = plotter.canvas

        if self.prev_plot is not None:
            """ remove previous plot """
            self.plot_space.removeWidget(self.prev_plot)

        i = self.plot_space.addWidget(util_canvas)
        self.plot_space.setCurrentIndex(i)

        nav = NavegationToolBar(util_canvas, self)
        if self.prev_nav is not None:
            self.tool_bar.removeWidget(self.prev_nav)
        i = self.tool_bar.addWidget(nav)
        self.tool_bar.setCurrentIndex(i)

    def count_down_callback(self):
        if self.media_player.processing():
            self.song_time = self.song_time.addSecs(-1)
            self.count_down.setText(self.song_time.toString("m:ss"))
        else:
            self.playing = False
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
        foo = []
        for i in range(0, len(sample)):
            foo.append((sample[i], self.all_callbacks[i]))

        out = np.array(list(map(self.effects_to_apply, foo)))
        return out[:, 0], out[:, 1]

    def effects_to_apply(self, var):
        func = var[1]
        return func(var[0])

    def effect_to_song(self):
        print('hola')

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
        temp.update_effect.connect(functools.partial(self.audio_procesing, index+1))
        temp.clicked.connect(self.get_back_effect)

    def audio_procesing(self, track_num):
        index = 0
        for i in range(0, len(self.working_tracks)):
            if self.working_tracks[i].me(track_num):
                index = i
                break
        index_2 = self.available_to_play.index(track_num-1)
        self.all_callbacks[index_2] = self.working_tracks[index].get_callback()

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
        self.plot_track.clear()
        """ Go to find new """
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Midi (*.mid)')
        """ If no file is selected quit """
        if filename == '':
            return

        """ Clear previous things"""
        self.disable_effect_enviroment()
        self.root = filename.split('.')[0]
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
        self.label.setText('Seleccione los instrumentos, y al sintetizar espere a que se pongan verdes los tracks')

        self.sintetizar.setDisabled(False)

    def create_tracks(self):

        """ working is a bool to avoid  conflicts while synthesizing """
        if not self.working:

            fin = len(self.track_manager)
            """ May be good looking to start a timer and do something meanwhile.. """
            self.working = True
            absents = []
            all_num = []


            for i in range(0, fin):
                all_num.append(i)
                volume, instrument = self.track_manager[i].get_data()
                self.backend.assign_instrument_to_track(i, instrument, volume/100.0)
                if volume == 0 or instrument == '':
                    absents.append(i)
                    self.backend.toggle_track(i)

            if len(absents) == len(self.track_manager):
                print('Compilando vacio')
                return

            for a in self.track_manager:  # This may be useful in future
                a.setStyleSheet(
                    'QWidget { border-style: solid; background-color: rgbrgb(81, 76, 149); border-radius: 5px;}')

            self.available_to_play = list(set(all_num).difference(set(absents)))
            self.progress_bar.setMaximum(len(self.available_to_play))
            self.progress_bar.setValue(0)
            self.progress_bar.show()

            self.backend.synthesize_song()
            self.fin()

    def progress_count(self, a):
        self.progress_bar.setValue(self.progress_bar.value() + 1)
        self.track_manager[a].setStyleSheet(
            'QWidget { border-style: solid; background-color: rgb(31, 172, 102); border-radius: 5px;}')

    def fin(self):
        #self.progress_bar.hide()
        self.enable_effects()
        self.plot_track.addItem('Plain Song')
        self.plot_track.addItems(['Track ' + str(i + 1) for i in self.available_to_play])
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
        song_len = np.ceil(song_len / 44100.0)
        self.song_time.setHMS(0, int(song_len / 60.0), int(song_len % 60))
        self.count_down.setText(self.song_time.toString("m:ss"))
        self.label.setText(
            'Ahora puede poner play, haciendo click sobre un track podrá seleccionalo para agregar efectos')

    def play(self):
        if self.media_buttons_widget.stop.isChecked():
            self.media_buttons_widget.stop.toggle()

        if self.playing:
            self.media_player.terminate_processing()
            song_len = len(self.all_tracks[0])
            song_len = np.ceil(song_len / 44100.0)
            self.song_time.setHMS(0, int(song_len / 60.0), int(song_len % 60))
            self.count_down.setText(self.song_time.toString("m:ss"))
            self.inner_timer.stop()
            for i in self.working_tracks:
                i.reset()
        self.playing = True

        self.media_player.start_non_blocking_processing()
        self.inner_timer.start(1000)

    def stop(self):
        if self.media_buttons_widget.play.isChecked():
            self.media_buttons_widget.play.toggle()
        if not self.playing:
            return
        self.playing = False
        self.media_player.terminate_processing()
        song_len = len(self.all_tracks[0])
        song_len = np.ceil(song_len / 44100.0)
        self.song_time.setHMS(0, int(song_len / 60.0), int(song_len % 60))
        self.count_down.setText(self.song_time.toString("m:ss"))
        self.inner_timer.stop()
        for i in self.working_tracks:
            i.reset()

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

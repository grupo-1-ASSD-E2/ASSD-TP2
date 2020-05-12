# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AudioTool(object):
    def setupUi(self, AudioTool):
        AudioTool.setObjectName("AudioTool")
        AudioTool.resize(570, 515)
        AudioTool.setStyleSheet("background-color: #6c7b95;")
        self.centralwidget = QtWidgets.QWidget(AudioTool)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Options = QtWidgets.QTabWidget(self.centralwidget)
        self.Options.setStyleSheet("")
        self.Options.setTabPosition(QtWidgets.QTabWidget.North)
        self.Options.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.Options.setElideMode(QtCore.Qt.ElideRight)
        self.Options.setUsesScrollButtons(True)
        self.Options.setDocumentMode(True)
        self.Options.setTabsClosable(False)
        self.Options.setMovable(True)
        self.Options.setTabBarAutoHide(True)
        self.Options.setObjectName("Options")
        self.Sintesis = QtWidgets.QWidget()
        self.Sintesis.setObjectName("Sintesis")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Sintesis)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_4 = QtWidgets.QWidget(self.Sintesis)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.select_file = QtWidgets.QPushButton(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_file.sizePolicy().hasHeightForWidth())
        self.select_file.setSizePolicy(sizePolicy)
        self.select_file.setStyleSheet(":active{\n"
"    image: url(:/botones/assets/buttons/file.png);\n"
"}\n"
"\n"
":hover{\n"
"    image: url(:/botones/assets/buttons/file_hoover.png);\n"
"}\n"
"\n"
":pres{\n"
"    image: url(:/botones/assets/buttons/file_press.png)\n"
"}")
        self.select_file.setText("")
        self.select_file.setObjectName("select_file")
        self.horizontalLayout_4.addWidget(self.select_file)
        self.midi_name = QtWidgets.QLabel(self.widget_4)
        self.midi_name.setStyleSheet("color: rgb(255, 255, 255);")
        self.midi_name.setObjectName("midi_name")
        self.horizontalLayout_4.addWidget(self.midi_name)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.view_zone = QtWidgets.QWidget(self.Sintesis)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view_zone.sizePolicy().hasHeightForWidth())
        self.view_zone.setSizePolicy(sizePolicy)
        self.view_zone.setObjectName("view_zone")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.view_zone)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.track_seter = QtWidgets.QWidget(self.view_zone)
        self.track_seter.setObjectName("track_seter")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.track_seter)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.track_set = QtWidgets.QScrollArea(self.track_seter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.track_set.sizePolicy().hasHeightForWidth())
        self.track_set.setSizePolicy(sizePolicy)
        self.track_set.setMinimumSize(QtCore.QSize(250, 0))
        self.track_set.setAutoFillBackground(True)
        self.track_set.setWidgetResizable(True)
        self.track_set.setObjectName("track_set")
        self.track_setter = QtWidgets.QWidget()
        self.track_setter.setGeometry(QtCore.QRect(0, 0, 248, 296))
        self.track_setter.setObjectName("track_setter")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.track_setter)
        self.verticalLayout.setObjectName("verticalLayout")
        self.track_0 = TrackConfigWidget(self.track_setter)
        self.track_0.setToolTip("")
        self.track_0.setAutoFillBackground(False)
        self.track_0.setStyleSheet("QWidget {\n"
"    border-style: solid;\n"
"    background-color: rgb(81, 76, 149);\n"
"    border-radius: 5px;\n"
"}\n"
"")
        self.track_0.setObjectName("track_0")
        self.verticalLayout.addWidget(self.track_0)
        spacerItem = QtWidgets.QSpacerItem(20, 215, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.track_set.setWidget(self.track_setter)
        self.verticalLayout_4.addWidget(self.track_set)
        self.sintetizar = QtWidgets.QPushButton(self.track_seter)
        self.sintetizar.setStyleSheet("color: rgb(255, 255, 255);")
        self.sintetizar.setObjectName("sintetizar")
        self.verticalLayout_4.addWidget(self.sintetizar)
        self.horizontalLayout_3.addWidget(self.track_seter)
        self.track_view = QtWidgets.QScrollArea(self.view_zone)
        self.track_view.setWidgetResizable(True)
        self.track_view.setObjectName("track_view")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 274, 326))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 215, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.track_view.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_3.addWidget(self.track_view)
        self.verticalLayout_2.addWidget(self.view_zone)
        self.buttom = QtWidgets.QWidget(self.Sintesis)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttom.sizePolicy().hasHeightForWidth())
        self.buttom.setSizePolicy(sizePolicy)
        self.buttom.setMaximumSize(QtCore.QSize(16777215, 50))
        self.buttom.setObjectName("buttom")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.buttom)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.wav_file = QtWidgets.QLabel(self.buttom)
        self.wav_file.setStyleSheet("color: rgb(255, 255, 255);")
        self.wav_file.setObjectName("wav_file")
        self.horizontalLayout_2.addWidget(self.wav_file)
        self.save = QtWidgets.QPushButton(self.buttom)
        self.save.setStyleSheet("color: rgb(255, 255, 255);")
        self.save.setObjectName("save")
        self.horizontalLayout_2.addWidget(self.save)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.media_buttons_widget = MediaButtonsWidget(self.buttom)
        self.media_buttons_widget.setObjectName("media_buttons_widget")
        self.horizontalLayout_2.addWidget(self.media_buttons_widget)
        self.verticalLayout_2.addWidget(self.buttom)
        self.Options.addTab(self.Sintesis, "")
        self.Efectos = QtWidgets.QWidget()
        self.Efectos.setObjectName("Efectos")
        self.Options.addTab(self.Efectos, "")
        self.horizontalLayout.addWidget(self.Options)
        AudioTool.setCentralWidget(self.centralwidget)

        self.retranslateUi(AudioTool)
        self.Options.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AudioTool)

    def retranslateUi(self, AudioTool):
        _translate = QtCore.QCoreApplication.translate
        AudioTool.setWindowTitle(_translate("AudioTool", "Audio tool"))
        self.midi_name.setText(_translate("AudioTool", "Choose midi file..."))
        self.track_0.setWhatsThis(_translate("AudioTool", "Track Config Widget.  "))
        self.sintetizar.setText(_translate("AudioTool", "Sintetizar"))
        self.label_3.setText(_translate("AudioTool", "Aca van a venir una visualizacion fachera de los traks"))
        self.wav_file.setText(_translate("AudioTool", "Wav file..."))
        self.save.setText(_translate("AudioTool", "Save"))
        self.media_buttons_widget.setToolTip(_translate("AudioTool", "Click and drag here"))
        self.media_buttons_widget.setWhatsThis(_translate("AudioTool", "Media buttons Widget.  "))
        self.Options.setTabText(self.Options.indexOf(self.Sintesis), _translate("AudioTool", "Sintesis"))
        self.Options.setTabText(self.Options.indexOf(self.Efectos), _translate("AudioTool", "Efectos"))

from FrontEnd.src.widgets.mediabutton import MediaButtonsWidget
from FrontEnd.src.widgets.trackconfig import TrackConfigWidget
from FrontEnd.src.resources import buttons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AudioTool = QtWidgets.QMainWindow()
    ui = Ui_AudioTool()
    ui.setupUi(AudioTool)
    AudioTool.show()
    sys.exit(app.exec_())


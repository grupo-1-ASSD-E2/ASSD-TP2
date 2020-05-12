# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\midi_instrument.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_track(object):
    def setupUi(self, track):
        track.setObjectName("track")
        track.resize(238, 50)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(150)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(track.sizePolicy().hasHeightForWidth())
        track.setSizePolicy(sizePolicy)
        track.setMinimumSize(QtCore.QSize(150, 50))
        track.setMaximumSize(QtCore.QSize(238, 50))
        track.setAutoFillBackground(False)
        track.setStyleSheet("QWidget {\n"
"    border-style: solid;\n"
"    background-color: rgb(81, 76, 149);\n"
"     border-radius: 5px;\n"
"}\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(track)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tracks_b = QtWidgets.QWidget(track)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tracks_b.sizePolicy().hasHeightForWidth())
        self.tracks_b.setSizePolicy(sizePolicy)
        self.tracks_b.setObjectName("tracks_b")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tracks_b)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.instrument = QtWidgets.QPushButton(self.tracks_b)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.instrument.sizePolicy().hasHeightForWidth())
        self.instrument.setSizePolicy(sizePolicy)
        self.instrument.setMinimumSize(QtCore.QSize(40, 0))
        self.instrument.setStyleSheet(":active {\n"
"    image:url(:/instruments/assets/instruments/nota.webp) 0 0 0 0;\n"
"}\n"
"\n"
":hover {\n"
"    image:url(:/instruments/assets/instruments/note.png) 0 0 0 0;\n"
"}\n"
"")
        self.instrument.setText("")
        self.instrument.setObjectName("instrument")
        self.horizontalLayout_2.addWidget(self.instrument)
        self.widget = QtWidgets.QWidget(self.tracks_b)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name = QtWidgets.QLabel(self.widget)
        self.name.setStyleSheet("color: rgb(255, 255, 255);")
        self.name.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.name.setObjectName("name")
        self.verticalLayout.addWidget(self.name)
        self.horizontalLayout_2.addWidget(self.widget)
        self.volume = QtWidgets.QSlider(self.tracks_b)
        self.volume.setMaximum(100)
        self.volume.setSliderPosition(100)
        self.volume.setOrientation(QtCore.Qt.Horizontal)
        self.volume.setInvertedAppearance(False)
        self.volume.setInvertedControls(False)
        self.volume.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.volume.setObjectName("volume")
        self.horizontalLayout_2.addWidget(self.volume)
        self.mute = QtWidgets.QPushButton(self.tracks_b)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mute.sizePolicy().hasHeightForWidth())
        self.mute.setSizePolicy(sizePolicy)
        self.mute.setStyleSheet(":active{\n"
"    border-image:url(:/botones/assets/buttons/sound.png);\n"
"}\n"
"\n"
":checked{\n"
"    border-image:url(:/botones/assets/buttons/mute.png);\n"
"}\n"
"")
        self.mute.setText("")
        self.mute.setCheckable(True)
        self.mute.setObjectName("mute")
        self.horizontalLayout_2.addWidget(self.mute)
        self.preview = QtWidgets.QCheckBox(self.tracks_b)
        self.preview.setText("")
        self.preview.setObjectName("preview")
        self.horizontalLayout_2.addWidget(self.preview)
        self.horizontalLayout.addWidget(self.tracks_b)

        self.retranslateUi(track)
        QtCore.QMetaObject.connectSlotsByName(track)

    def retranslateUi(self, track):
        _translate = QtCore.QCoreApplication.translate
        track.setWindowTitle(_translate("track", "Form"))
        self.name.setText(_translate("track", "Track N"))
        self.mute.setToolTip(_translate("track", "mute/unmute"))

from FrontEnd.src.resources import buttons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    track = QtWidgets.QWidget()
    ui = Ui_track()
    ui.setupUi(track)
    track.show()
    sys.exit(app.exec_())


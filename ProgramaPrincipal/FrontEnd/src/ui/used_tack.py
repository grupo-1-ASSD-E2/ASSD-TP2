# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\used_tack.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_worked_track(object):
    def setupUi(self, worked_track):
        worked_track.setObjectName("worked_track")
        worked_track.resize(564, 60)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(worked_track.sizePolicy().hasHeightForWidth())
        worked_track.setSizePolicy(sizePolicy)
        worked_track.setMinimumSize(QtCore.QSize(0, 60))
        worked_track.setMaximumSize(QtCore.QSize(16777215, 60))
        worked_track.setStyleSheet("QWidget{\n"
"    border-radius: 3px;\n"
"    background-color: rgb(255, 200, 88);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(worked_track)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(worked_track)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.track = QtWidgets.QLabel(self.widget)
        self.track.setObjectName("track")
        self.horizontalLayout.addWidget(self.track)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.effect = QtWidgets.QLabel(self.widget)
        self.effect.setObjectName("effect")
        self.horizontalLayout.addWidget(self.effect)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.mute = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mute.sizePolicy().hasHeightForWidth())
        self.mute.setSizePolicy(sizePolicy)
        self.mute.setStyleSheet(":active{\n"
"    image: url(:/botones/assets/buttons/sound.png);\n"
"}\n"
"\n"
":checked{\n"
"    border-image:url(:/botones/assets/buttons/mute.png);\n"
"}")
        self.mute.setText("")
        self.mute.setCheckable(True)
        self.mute.setObjectName("mute")
        self.horizontalLayout.addWidget(self.mute)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(worked_track)
        QtCore.QMetaObject.connectSlotsByName(worked_track)

    def retranslateUi(self, worked_track):
        _translate = QtCore.QCoreApplication.translate
        worked_track.setWindowTitle(_translate("worked_track", "Form"))
        self.track.setText(_translate("worked_track", "Track N"))
        self.label.setText(_translate("worked_track", "-"))
        self.effect.setText(_translate("worked_track", "Effect"))

from FrontEnd.src.resources import buttons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    worked_track = QtWidgets.QWidget()
    ui = Ui_worked_track()
    ui.setupUi(worked_track)
    worked_track.show()
    sys.exit(app.exec_())


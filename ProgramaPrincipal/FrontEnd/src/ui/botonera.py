# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\botonera.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MediaObject(object):
    def setupUi(self, MediaObject):
        MediaObject.setObjectName("MediaObject")
        MediaObject.resize(150, 50)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MediaObject.sizePolicy().hasHeightForWidth())
        MediaObject.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(MediaObject)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pause = QtWidgets.QPushButton(MediaObject)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pause.sizePolicy().hasHeightForWidth())
        self.pause.setSizePolicy(sizePolicy)
        self.pause.setStyleSheet(":active{\n"
"    border-image:url(:/botones/assets/buttons/pause.png) 0 0 0 0;\n"
"}\n"
"\n"
":checked{\n"
"    border-image:url(:/botones/assets/buttons/pause_on.png) 0 0 0 0;\n"
"}\n"
"")
        self.pause.setText("")
        self.pause.setCheckable(True)
        self.pause.setObjectName("pause")
        self.horizontalLayout.addWidget(self.pause)
        self.play = QtWidgets.QPushButton(MediaObject)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.play.sizePolicy().hasHeightForWidth())
        self.play.setSizePolicy(sizePolicy)
        self.play.setStyleSheet(":active{\n"
"    border-image:url(:/botones/assets/buttons/play.png) 0 0 0 0;\n"
"}\n"
"\n"
":checked{\n"
"    border-image:url(:/botones/assets/buttons/play_on.png) 0 0 0 0;\n"
"}\n"
"")
        self.play.setText("")
        self.play.setCheckable(True)
        self.play.setObjectName("play")
        self.horizontalLayout.addWidget(self.play)
        self.stop = QtWidgets.QPushButton(MediaObject)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop.sizePolicy().hasHeightForWidth())
        self.stop.setSizePolicy(sizePolicy)
        self.stop.setStyleSheet(":active{\n"
"    border-image:url(:/botones/assets/buttons/stop.png) ;\n"
"}\n"
"\n"
":checked{\n"
"    border-image: url(:/botones/assets/buttons/stop_on.png) ;\n"
"\n"
"}\n"
"")
        self.stop.setText("")
        self.stop.setCheckable(True)
        self.stop.setObjectName("stop")
        self.horizontalLayout.addWidget(self.stop)

        self.retranslateUi(MediaObject)
        QtCore.QMetaObject.connectSlotsByName(MediaObject)

    def retranslateUi(self, MediaObject):
        _translate = QtCore.QCoreApplication.translate
        MediaObject.setWindowTitle(_translate("MediaObject", "Form"))

from FrontEnd.src.resources import buttons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MediaObject = QtWidgets.QWidget()
    ui = Ui_MediaObject()
    ui.setupUi(MediaObject)
    MediaObject.show()
    sys.exit(app.exec_())


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
        MediaObject.resize(151, 50)
        self.horizontalLayout = QtWidgets.QHBoxLayout(MediaObject)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(MediaObject)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setStyleSheet(":active{\n"
"    border-image:url(:/botones/assets/buttons/pause.png) 0 0 0 0;\n"
"}\n"
"")
        self.pushButton.setText("")
        self.pushButton.setCheckable(True)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(MediaObject)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setStyleSheet(":active{\n"
"    border-image:url(:/botones/assets/buttons/play.png) 0 0 0 0;\n"
"}\n"
"\n"
":checked{\n"
"    border-image:url(:/botones/assets/buttons/play_on.png) 0 0 0 0;\n"
"}\n"
"")
        self.pushButton_2.setText("")
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(MediaObject)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setStyleSheet(":active{\n"
"    border-image:url(:/botones/assets/buttons/stop.png) ;\n"
"}\n"
"\n"
":checked{\n"
"    border-image: url(:/botones/assets/buttons/stop_on.png) ;\n"
"\n"
"}\n"
"")
        self.pushButton_3.setText("")
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)

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


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\instruments.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Instruments(object):
    def setupUi(self, Instruments):
        Instruments.setObjectName("Instruments")
        Instruments.resize(300, 250)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Instruments.sizePolicy().hasHeightForWidth())
        Instruments.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/instruments/assets/instruments/piano.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Instruments.setWindowIcon(icon)
        Instruments.setStyleSheet("QWidget{\n"
"    background-color: #6c7b95;\n"
"}\n"
"QPushButton {\n"
"    background-color: rgb(81, 76, 149);\n"
"}\n"
"\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(Instruments)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Instruments)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.button_collector = QtWidgets.QWidget(Instruments)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_collector.sizePolicy().hasHeightForWidth())
        self.button_collector.setSizePolicy(sizePolicy)
        self.button_collector.setObjectName("button_collector")
        self.gridLayout = QtWidgets.QGridLayout(self.button_collector)
        self.gridLayout.setObjectName("gridLayout")
        self.base_button_4 = QtWidgets.QPushButton(self.button_collector)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.base_button_4.sizePolicy().hasHeightForWidth())
        self.base_button_4.setSizePolicy(sizePolicy)
        self.base_button_4.setMinimumSize(QtCore.QSize(50, 50))
        self.base_button_4.setMaximumSize(QtCore.QSize(50, 50))
        self.base_button_4.setStyleSheet("")
        self.base_button_4.setText("")
        self.base_button_4.setObjectName("base_button_4")
        self.gridLayout.addWidget(self.base_button_4, 0, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.verticalLayout.addWidget(self.button_collector)
        self.verticalLayout.setStretch(0, 3)

        self.retranslateUi(Instruments)
        QtCore.QMetaObject.connectSlotsByName(Instruments)

    def retranslateUi(self, Instruments):
        _translate = QtCore.QCoreApplication.translate
        Instruments.setWindowTitle(_translate("Instruments", "Instruments"))
        self.label.setText(_translate("Instruments", "Elija un Instrumento"))

from FrontEnd.src.resources import buttons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Instruments = QtWidgets.QWidget()
    ui = Ui_Instruments()
    ui.setupUi(Instruments)
    Instruments.show()
    sys.exit(app.exec_())


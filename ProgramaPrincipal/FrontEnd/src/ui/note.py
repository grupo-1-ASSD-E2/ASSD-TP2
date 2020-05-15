# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\note.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(568, 60)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 60))
        Form.setMaximumSize(QtCore.QSize(16777215, 60))
        Form.setStyleSheet("QWidget{\n"
"    border-radius: 3px;\n"
"    background-color: rgb(255, 163, 51);\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.freq = QtWidgets.QLabel(self.widget)
        self.freq.setObjectName("freq")
        self.horizontalLayout_2.addWidget(self.freq)
        self.init = QtWidgets.QLabel(self.widget)
        self.init.setObjectName("init")
        self.horizontalLayout_2.addWidget(self.init)
        self.long_2 = QtWidgets.QLabel(self.widget)
        self.long_2.setObjectName("long_2")
        self.horizontalLayout_2.addWidget(self.long_2)
        self.col = QtWidgets.QLabel(self.widget)
        self.col.setObjectName("col")
        self.horizontalLayout_2.addWidget(self.col)
        self.inst = QtWidgets.QLabel(self.widget)
        self.inst.setObjectName("inst")
        self.horizontalLayout_2.addWidget(self.inst)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setStyleSheet("image: url(:/botones/assets/buttons/cross.png);")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.freq.setText(_translate("Form", "freq"))
        self.init.setText(_translate("Form", "t inicio"))
        self.long_2.setText(_translate("Form", "duracion"))
        self.col.setText(_translate("Form", "velocity"))
        self.inst.setText(_translate("Form", "Instrumento"))

from FrontEnd.src.resources import buttons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())


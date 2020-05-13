# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\effect_property.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_e_prop(object):
    def setupUi(self, e_prop):
        e_prop.setObjectName("e_prop")
        e_prop.resize(140, 190)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(e_prop.sizePolicy().hasHeightForWidth())
        e_prop.setSizePolicy(sizePolicy)
        e_prop.setMinimumSize(QtCore.QSize(140, 190))
        e_prop.setMaximumSize(QtCore.QSize(140, 190))
        self.verticalLayout = QtWidgets.QVBoxLayout(e_prop)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(e_prop)
        self.frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Prop = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.Prop.setFont(font)
        self.Prop.setTextFormat(QtCore.Qt.PlainText)
        self.Prop.setScaledContents(True)
        self.Prop.setAlignment(QtCore.Qt.AlignCenter)
        self.Prop.setWordWrap(True)
        self.Prop.setObjectName("Prop")
        self.verticalLayout_2.addWidget(self.Prop)
        self.preset = QtWidgets.QDial(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preset.sizePolicy().hasHeightForWidth())
        self.preset.setSizePolicy(sizePolicy)
        self.preset.setMaximum(100)
        self.preset.setSingleStep(1)
        self.preset.setProperty("value", 0)
        self.preset.setSliderPosition(0)
        self.preset.setTracking(False)
        self.preset.setWrapping(True)
        self.preset.setNotchesVisible(True)
        self.preset.setObjectName("preset")
        self.verticalLayout_2.addWidget(self.preset)
        self.value = QtWidgets.QLabel(self.frame)
        self.value.setStyleSheet("border-radius: 3px;\n"
"background-color: rgb(128, 202, 44);")
        self.value.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.value.setAlignment(QtCore.Qt.AlignCenter)
        self.value.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.value.setObjectName("value")
        self.verticalLayout_2.addWidget(self.value)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(e_prop)
        QtCore.QMetaObject.connectSlotsByName(e_prop)

    def retranslateUi(self, e_prop):
        _translate = QtCore.QCoreApplication.translate
        e_prop.setWindowTitle(_translate("e_prop", "Form"))
        self.Prop.setText(_translate("e_prop", "Prop"))
        self.value.setText(_translate("e_prop", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    e_prop = QtWidgets.QWidget()
    ui = Ui_e_prop()
    ui.setupUi(e_prop)
    e_prop.show()
    sys.exit(app.exec_())


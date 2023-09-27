# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\UART_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(474, 189)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 4, 1, 1)
        self.comboBox_Speed = QtWidgets.QComboBox(Dialog)
        self.comboBox_Speed.setObjectName("comboBox_Speed")
        self.gridLayout.addWidget(self.comboBox_Speed, 0, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.comboBox_DataBits = QtWidgets.QComboBox(Dialog)
        self.comboBox_DataBits.setObjectName("comboBox_DataBits")
        self.gridLayout.addWidget(self.comboBox_DataBits, 1, 1, 1, 1)
        self.comboBox_StopBits = QtWidgets.QComboBox(Dialog)
        self.comboBox_StopBits.setObjectName("comboBox_StopBits")
        self.gridLayout.addWidget(self.comboBox_StopBits, 1, 3, 1, 1)
        self.comboBox_Parity = QtWidgets.QComboBox(Dialog)
        self.comboBox_Parity.setObjectName("comboBox_Parity")
        self.gridLayout.addWidget(self.comboBox_Parity, 1, 5, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.checkBox_RtsCts = QtWidgets.QCheckBox(Dialog)
        self.checkBox_RtsCts.setObjectName("checkBox_RtsCts")
        self.gridLayout.addWidget(self.checkBox_RtsCts, 2, 1, 1, 1)
        self.checkBox_DsrDtr = QtWidgets.QCheckBox(Dialog)
        self.checkBox_DsrDtr.setObjectName("checkBox_DsrDtr")
        self.gridLayout.addWidget(self.checkBox_DsrDtr, 2, 3, 1, 1)
        self.checkBox_XonXoff = QtWidgets.QCheckBox(Dialog)
        self.checkBox_XonXoff.setObjectName("checkBox_XonXoff")
        self.gridLayout.addWidget(self.checkBox_XonXoff, 2, 5, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 6)
        self.comboBox_ComPort = QtWidgets.QComboBox(Dialog)
        self.comboBox_ComPort.setObjectName("comboBox_ComPort")
        self.gridLayout.addWidget(self.comboBox_ComPort, 0, 1, 1, 3)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.checkBox_SetTimeDate = QtWidgets.QCheckBox(Dialog)
        self.checkBox_SetTimeDate.setObjectName("checkBox_SetTimeDate")
        self.gridLayout.addWidget(self.checkBox_SetTimeDate, 4, 1, 1, 5)
        self.checkBox_skipInitialSetup = QtWidgets.QCheckBox(Dialog)
        self.checkBox_skipInitialSetup.setObjectName("checkBox_skipInitialSetup")
        self.gridLayout.addWidget(self.checkBox_skipInitialSetup, 3, 1, 1, 5)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "COM port"))
        self.label_5.setText(_translate("Dialog", "Speed"))
        self.label_2.setText(_translate("Dialog", "Data bits"))
        self.label_4.setText(_translate("Dialog", "Parity"))
        self.label_6.setText(_translate("Dialog", "Flow control"))
        self.label_3.setText(_translate("Dialog", "Stop bits"))
        self.checkBox_RtsCts.setText(_translate("Dialog", "RTS/CTS"))
        self.checkBox_DsrDtr.setText(_translate("Dialog", "DSR/DTR"))
        self.checkBox_XonXoff.setText(_translate("Dialog", "XON/XOFF"))
        self.label_7.setText(_translate("Dialog", "Telescope"))
        self.checkBox_SetTimeDate.setText(_translate("Dialog", "Set current date and time"))
        self.checkBox_skipInitialSetup.setText(_translate("Dialog", "Skip initial setup"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


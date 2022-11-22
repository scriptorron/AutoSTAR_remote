"""
UART interface for AutoSTAR_remote
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import serial
import serial.tools.list_ports

import UART_ui


class UART(QtWidgets.QDialog):

    def __init__(self, Parameter={}):
        super().__init__()
        self.ui = UART_ui.Ui_Dialog()
        self.ui.setupUi(self)
        # populate GUI
        self.find_Ports()
        self.ui.comboBox_ComPort.addItems([p["desc"] for p in self.KnownPorts])
        self.ui.comboBox_Speed.addItems([f'{s}' for s in [
            50, 75, 110, 134, 150, 200, 300, 600, 1200,
            1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200
        ]])
        self.ui.comboBox_DataBits.addItems([f'{b}' for b in [5, 6, 7, 8]])
        self.ui.comboBox_StopBits.addItems(["1", "1.5", "2"])
        self.ui.comboBox_Parity.addItems(["none", "even", "odd", "mark", "space"])
        self.ui.checkBox_RtsCts.setChecked(False)
        self.ui.checkBox_DsrDtr.setChecked(False)
        self.ui.checkBox_XonXoff.setChecked(False)
        self.ui.checkBox_SetTimeDate.setChecked(True)
        # set defaults
        self.set_Parameter(Parameter)
        # no port opened
        self.PortHandle = None
        self.Name = ""

    def get_Parameter(self):
        Parameter = {
            "port": self.KnownPorts[self.ui.comboBox_ComPort.currentIndex()]["port"],
            "baudrate": self.ui.comboBox_Speed.currentText(),
            "bytesize": self.ui.comboBox_DataBits.currentText(),
            "parity": self.ui.comboBox_Parity.currentText(),
            "stopbits": self.ui.comboBox_StopBits.currentText(),
            "xonxoff": str(self.ui.checkBox_XonXoff.isChecked()),
            "rtscts": str(self.ui.checkBox_RtsCts.isChecked()),
            "dsrdtr": str(self.ui.checkBox_DsrDtr.isChecked()),
            "setTimeDate": str(self.ui.checkBox_SetTimeDate.isChecked()),
        }
        return Parameter

    def set_Parameter(self, Parameter):
        for i in range(self.ui.comboBox_ComPort.count()):
            if self.KnownPorts[i]["port"] == Parameter.get("port", ""):
                self.ui.comboBox_ComPort.setCurrentIndex(i)
                break
        def set_Current(cb, text):
            for j in range(cb.count()):
                if cb.itemText(j) == text:
                    cb.setCurrentIndex(j)
                    break
        set_Current(self.ui.comboBox_Speed, Parameter.get("baudrate", "9600"))
        set_Current(self.ui.comboBox_DataBits, Parameter.get("bytesize", "8"))
        set_Current(self.ui.comboBox_Parity, Parameter.get("parity", "none"))
        set_Current(self.ui.comboBox_StopBits, Parameter.get("stopbits", "1"))
        self.ui.checkBox_XonXoff.setChecked(Parameter.get("xonxoff", "") == "True")
        self.ui.checkBox_RtsCts.setChecked(Parameter.get("rtscts", "") == "True")
        self.ui.checkBox_DsrDtr.setChecked(Parameter.get("dsrdtr", "") == "True")
        self.ui.checkBox_SetTimeDate.setChecked(Parameter.get("setDateTime", "True") == "True")

    def find_Ports(self, include_links=False):
        iterator = sorted(serial.tools.list_ports.comports(include_links=include_links))
        self.KnownPorts = []
        for port, desc, hwid in iterator:
            self.KnownPorts.append({"port": port, "desc": desc, "hwid": hwid})

    def open(self, timeout=2.0, write_timeout=None, inter_byte_timeout=None, exclusive=False):
        ret = self.exec_()
        if ret == self.Accepted:
            self.Name = self.ui.comboBox_ComPort.currentText()
            port = self.KnownPorts[self.ui.comboBox_ComPort.currentIndex()]["port"]
            baudrate = int(self.ui.comboBox_Speed.currentText())
            bytesize = {
                "5": serial.FIVEBITS, "6": serial.SIXBITS, "7": serial.SEVENBITS, "8": serial.EIGHTBITS
            }[self.ui.comboBox_DataBits.currentText()]
            parity = {
                "none": serial.PARITY_NONE, "even": serial.PARITY_EVEN, "odd": serial.PARITY_ODD,
                "mark": serial.PARITY_MARK, "space": serial.PARITY_SPACE
            }[self.ui.comboBox_Parity.currentText()]
            stopbits = {
                "1": serial.STOPBITS_ONE, "1.5": serial.STOPBITS_ONE_POINT_FIVE, "2": serial.STOPBITS_TWO
            }[self.ui.comboBox_StopBits.currentText()]
            xonxoff = self.ui.checkBox_XonXoff.isChecked()
            rtscts = self.ui.checkBox_RtsCts.isChecked()
            dsrdtr = self.ui.checkBox_DsrDtr.isChecked()
            if os.name == "nt":
                # windows supports exclusive access only!
                exclusive = True
            try:
                self.PortHandle = serial.Serial(
                    port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits,
                    timeout=timeout, xonxoff=xonxoff, rtscts=rtscts, dsrdtr=dsrdtr, write_timeout=write_timeout,
                    inter_byte_timeout=inter_byte_timeout, exclusive=exclusive
                )
            except serial.SerialException as e:
                QtWidgets.QMessageBox.critical(None, "Can not open UART port!", f"{e}")
                self.PortHandle = None

    def is_open(self):
        if self.PortHandle is not None:
            return self.PortHandle.is_open
        else:
            return False

    def close(self):
        if self.PortHandle is not None:
            self.PortHandle.close()
        self.PortHandle = None
        self.Name = ""

    def sendCommandBlind(self, cmd):
        if self.is_open():
            MeadeCmd = f'#:{cmd}#'.encode("ascii")
            self.PortHandle.write(MeadeCmd)

    def sendCommandString(self, cmd):
        if self.is_open():
            MeadeCmd = f'#:{cmd}#'.encode("ascii")
            print(f'sendCommandString command: {MeadeCmd}')
            self.PortHandle.write(MeadeCmd)
            Response = self.PortHandle.read_until("#".encode("ascii"))
            print(f'sendCommandString response: {Response}')
            Response = Response.rstrip("#".encode("ascii"))
            Response = Response.decode("utf-16")
            return Response
        return None


if __name__ == '__main__':
    # for debugging only
    theme_selection = "Dark"  # "Dark", "Light"
    App = QtWidgets.QApplication(sys.argv)
    App.setOrganizationName("GeierSoft")
    App.setOrganizationDomain("Astro")
    App.setApplicationName("AutoSTAR_remote")
    # copied from https://stackoverflow.com/questions/48256772/dark-theme-for-qt-widgets
    if theme_selection == 'Dark':
        App.setStyle("Fusion")
        #
        # # Now use a palette to switch to dark colors:
        dark_palette = QtGui.QPalette()
        dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(35, 35, 35))
        dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(25, 25, 25))
        dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
        dark_palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(35, 35, 35))
        dark_palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtCore.Qt.darkGray)
        dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtCore.Qt.darkGray)
        dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtCore.Qt.darkGray)
        dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, QtGui.QColor(53, 53, 53))
        App.setPalette(dark_palette)
    elif theme_selection == 'Light':
        App.setStyle("")
        pass
    else:
        pass
    #
    UartDialog = UART()
    UartDialog.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sys.exit(App.exec_())

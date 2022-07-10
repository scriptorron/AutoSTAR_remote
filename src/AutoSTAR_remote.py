"""
This is a remote control program for the Meade #497 telescope control.
It requires the Meade ASCOM driver.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import win32com.client

import AutoSTAR_remote_ui

version = "V1.0"

theme_selection = "Dark" # "Dark", "Light"
LCD_polling_time = 1000 # milliseconds

"""
By watching the RS232 communication of the AutoStart Suit telescope control I found the following commands: 
- on a regular base the display is read with :ED#
- more seldom but also regular the telescop position is read with :GR# and :GD#
- the buttons send the following commands:
  + ENTER :EK13#
  + long ENTER :EK10#
  + MODE :EK9#
  + long MODE :EK11#
  + GOTO :EK24#
  + long GOTO :EK25#
  + North :Mn# when button gets pressed, :Qn# when button gets released
  + West :Me# when button gets pressed, :Qw# when button gets released (yes, West sends the slew east command!)
  + East :Mw# when button gets pressed, :Qe# when button gets released (yes, West sends the slew west command!)
  + South :Ms# when button gets pressed, :Qs# when button gets released
  + 1 :EK49#
  + 2 :EK50#
  + 3 :EK51#
  + 4 :EK52#
  + 5 :EK53#
  + 6 :EK54#
  + 7 :EK55#
  + 8 :EK56#
  + 9 :EK57#
  + 0 :EK48#
  + Foc.In :F-# repeated as long as the button is pressed, :FQ# when button gets released
  + Foc. Out :F+# repeated as long as the button is pressed, :FQ# when button gets released
  + Scroll Up :EK94#
  + Scroll Down :EK118#
  + Back :EK87#
  + Fwd :EK69#
  + ? :EK63#
"""

class MainWin(QtWidgets.QMainWindow):
    """
    AutoSTAR_remote main window.
    """

    def __init__(self):
        super(MainWin, self).__init__()
        self.ui = AutoSTAR_remote_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f'AutoSTAR_remote {version}')
        font = QtGui.QFont("monospace")
        font.setStyleHint(QtGui.QFont.TypeWriter)
        font.setPointSizeF(10)
        self.ui.plainTextEdit_LCD.setFont(font)
        # states
        self.Telescope = None
        self.TelescopeName = ""
        # LCD polling timer
        self.PollingTimer = QtCore.QTimer()
        self.PollingTimer.setSingleShot(True)
        self.PollingTimer.setInterval(LCD_polling_time)
        self.PollingTimer.timeout.connect(self.updateLCD)
        # connect buttons
        self.ui.pushButton_Enter.clicked.connect(lambda: self.buttonAction("EK13", "EK10"))
        self.ui.pushButton_Mode.clicked.connect(lambda: self.buttonAction("EK9", "EK11"))
        self.ui.pushButton_Goto.clicked.connect(lambda: self.buttonAction("EK24", "EK25"))
        self.ui.pushButton_Num1.clicked.connect(lambda: self.buttonAction("EK49"))
        self.ui.pushButton_Num2.clicked.connect(lambda: self.buttonAction("EK50"))
        self.ui.pushButton_Num3.clicked.connect(lambda: self.buttonAction("EK51"))
        self.ui.pushButton_Num4.clicked.connect(lambda: self.buttonAction("EK52"))
        self.ui.pushButton_Num5.clicked.connect(lambda: self.buttonAction("EK53"))
        self.ui.pushButton_Num6.clicked.connect(lambda: self.buttonAction("EK54"))
        self.ui.pushButton_Num7.clicked.connect(lambda: self.buttonAction("EK55"))
        self.ui.pushButton_Num8.clicked.connect(lambda: self.buttonAction("EK56"))
        self.ui.pushButton_Num9.clicked.connect(lambda: self.buttonAction("EK57"))
        self.ui.pushButton_Num0.clicked.connect(lambda: self.buttonAction("EK48"))
        self.ui.pushButton_ScrollUp.clicked.connect(lambda: self.buttonAction("EK94"))
        self.ui.pushButton_ScrollDown.clicked.connect(lambda: self.buttonAction("EK118"))
        self.ui.pushButton_Back.clicked.connect(lambda: self.buttonAction("EK87"))
        self.ui.pushButton_Fwd.clicked.connect(lambda: self.buttonAction("EK69"))
        self.ui.pushButton_Help.clicked.connect(lambda: self.buttonAction("EK63"))
        # some buttons have actions when pressed and released
        self.ui.pushButton_North.pressed.connect(lambda: self.sendCommandBlind("Mn"))
        self.ui.pushButton_North.released.connect(lambda: self.sendCommandBlind("Qn"))
        self.ui.pushButton_West.pressed.connect(lambda: self.sendCommandBlind("Me"))
        self.ui.pushButton_West.released.connect(lambda: self.sendCommandBlind("Qw"))
        self.ui.pushButton_East.pressed.connect(lambda: self.sendCommandBlind("Mw"))
        self.ui.pushButton_East.released.connect(lambda: self.sendCommandBlind("Qe"))
        self.ui.pushButton_South.pressed.connect(lambda: self.sendCommandBlind("Ms"))
        self.ui.pushButton_South.released.connect(lambda: self.sendCommandBlind("Qs"))
        #
        self.ui.pushButton_FocIn.pressed.connect(lambda: self.sendCommandBlind("F-"))
        self.ui.pushButton_FocIn.released.connect(lambda: self.sendCommandBlind("FQ"))
        self.ui.pushButton_FocOut.pressed.connect(lambda: self.sendCommandBlind("F+"))
        self.ui.pushButton_FocOut.released.connect(lambda: self.sendCommandBlind("FQ"))


    @QtCore.pyqtSlot()
    def closeEvent(self, event):
        self.PollingTimer.stop()
        if self.Telescope is not None:
            if self.Telescope.Connected:
                self.Telescope.Connected = False
        # proceed with close
        event.accept()

    @QtCore.pyqtSlot()
    def on_actionconnect_triggered(self):
        try:
            Chooser  = win32com.client.Dispatch("ASCOM.Utilities.Chooser")
        except win32com.client.pywintypes.com_error:
            QtWidgets.QMessageBox.critical(None, "Can not call ASCOM!",
                                           f"Is ASCOM installed?")
            return
        Chooser.DeviceType = 'Telescope'
        self.TelescopeName = Chooser.Choose(None)
        self.ui.statusbar.showMessage(self.TelescopeName)
        self.Telescope = win32com.client.Dispatch(self.TelescopeName)
        self.Telescope.Connected = True
        if not self.Telescope.Connected:
            QtWidgets.QMessageBox.critical(None, "Can not connect to telescope!",
                                           f"Please check connection to\n{self.TelescopeName}.\nMaybe it is already in use.")
        else:
            self.ui.actionconnect.setEnabled(False)
            self.ui.actiondisconnect.setEnabled(True)
            self.ui.centralwidget.setEnabled(True)
            if self.ui.actionpoll.isChecked():
                self.PollingTimer.start()
            self.ui.actionupdate_now.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_actiondisconnect_triggered(self):
        self.PollingTimer.stop()
        if self.Telescope is not None:
            if self.Telescope.Connected:
                self.Telescope.Connected = False
                self.ui.actionconnect.setEnabled(True)
                self.ui.actiondisconnect.setEnabled(False)
                self.ui.centralwidget.setEnabled(False)
                self.ui.actionupdate_now.setEnabled(False)

    def sendAction(self, param):
        if self.Telescope is not None:
            if self.Telescope.Connected:
                return self.Telescope.Action("handbox", param)
        return None

    def sendCommandBlind(self, cmd):
        if self.Telescope is not None:
            if self.Telescope.Connected:
                return self.Telescope.CommandBlind(cmd, False)
        return None

    def buttonAction(self, cmd, long_cmd=None):
        """
        check if button was pressed with SHIFT and send commands cmd or cmd_long
        :param cmd: command for normal button click
        :param long_cmd: command for SHIFT+button click; if None -> use cmd
        """
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if (modifiers == QtCore.Qt.ShiftModifier) and (long_cmd is not None):
            self.sendCommandBlind(long_cmd)
        else:
            self.sendCommandBlind(cmd)
        self.updateLCD()

    # The :ED# command sends the LCD contents, coded withthe char table of the SED1233 LCD controller.
    # For any reason the COM interface or the win32com transforms this into unicode. Unfortunately the
    # special characters of the SED1233 controller get mapped to the wrong unicode. Here we fix this
    # with a translation table:
    CharacterTranslationTable = {
        0x0d: ord('\n'),
        #0x2020: ord(' '),
        0xDF: ord('°'),
        0x7E: 0x2192, #ord('>'),
        0x7F: 0x2190, #ord('<'),
        0x18: 0x2191, #ord('^'),
        0x19: 0x2193, #ord('v'),
        # bar graph symbols
        0x5F: 0x2582,
        0x81: 0x2583,
        0x201A: 0x2584, # raw: 0x82
        0x0192: 0x2585, # raw: 0x83
        0x201E: 0x2586, # raw: 0x84
        0x2026: 0x2587, # raw: 0x85
        0x2020: 0x2588, # raw: 0x86
    }

    def updateLCD(self):
        #LcdText = self.sendAction("readdisplay")
        LcdText = self.Telescope.CommandString("ED", False)
        if LcdText is not None:
            LcdText = LcdText.translate(self.CharacterTranslationTable)
            Unknown = ord(LcdText[0])
            Line1 = LcdText[1:17]
            Line2 = LcdText[17:]
            self.ui.plainTextEdit_LCD.setPlainText(f'{Line1}\n{Line2}')
            #print(f'{Unknown}: >{Line1}< >{Line2}<')
            #print(", ".join([f'{ord(c):02X}' for c in LcdText]))
            #print(bytes(LcdText, 'utf-8'))
        if self.ui.actionpoll.isChecked():
            self.PollingTimer.start()

    @QtCore.pyqtSlot()
    def on_actionupdate_now_triggered(self):
        self.updateLCD()

    @QtCore.pyqtSlot("bool")
    def on_actionpoll_toggled(self, isChecked):
        if isChecked:
            # start polling timer
            self.PollingTimer.start()
        else:
            # stop polling timer
            self.PollingTimer.stop()


## Start Qt event loop unless running in interactive mode.
def main():
    # build application
    App = QtWidgets.QApplication(sys.argv)
    App.setOrganizationName("GeierSoft")
    App.setOrganizationDomain("Astro")
    App.setApplicationName("AutoSTAR_remote")
    #
    # stolen from https://stackoverflow.com/questions/48256772/dark-theme-for-qt-widgets
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
    MainWindow = MainWin()
    #MainWindow.resize(1400, 900)
    MainWindow.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        #QtGui.QApplication.instance().exec_()
        sys.exit(App.exec_())


if __name__ == '__main__':
    main()
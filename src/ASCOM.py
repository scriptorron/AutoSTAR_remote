"""
ASCOM interface for AutoSTAR_remote
"""

from PyQt5 import QtWidgets
import win32com.client


class ASCOM:

    def __init__(self):
        self.Telescope = None
        self.Name = ""

    def open(self):
        self.close()
        try:
            Chooser = win32com.client.Dispatch("ASCOM.Utilities.Chooser")
        except win32com.client.pywintypes.com_error:
            QtWidgets.QMessageBox.critical(None, "Can not call ASCOM!",
                                           f"Is ASCOM installed?")
        else:
            Chooser.DeviceType = 'Telescope'
            self.Name = Chooser.Choose(None)
            if self.Name != "":
                self.Telescope = win32com.client.Dispatch(self.Name)
                self.Telescope.Connected = True
                if not self.Telescope.Connected:
                    QtWidgets.QMessageBox.critical(None, "Can not connect to telescope!",
                                                   f"Please check connection to\n{self.Name}.\nMaybe it is already in use.")
                    self.Telescope = None

    def get_Parameter(self):
        # has no parameter
        return dict()

    def is_open(self):
        if self.Telescope is not None:
            if self.Telescope.Connected:
                return True
        return False

    def close(self):
        if self.is_open():
            self.Telescope.Connected = False
        self.Telescope = None
        self.Name = ""

    def sendCommandBlind(self, cmd):
        if self.is_open():
            try:
                ret = self.Telescope.CommandBlind(cmd, False)
            except win32com.client.pywintypes.com_error as e:
                print(f'sendCommandBlind: {e}')
                return None
            else:
                return ret
        return None

    # The :ED# command sends the LCD contents, coded with the char table of the SED1233 LCD controller.
    # For any reason the COM interface or the win32com transforms this into unicode. Unfortunately the
    # special characters of the SED1233 controller get mapped to the wrong unicode. Here we fix this
    # with a translation table:
    CharacterTranslationTable = {
        0x0d: ord('\n'),
        # 0x2020: ord(' '),
        0xDF: ord('°'),
        0x7E: 0x2192,  # ord('>'),
        0x7F: 0x2190,  # ord('<'),
        0x18: 0x2191,  # ord('^'),
        0x19: 0x2193,  # ord('v'),
        # bar graph symbols
        0x5F: 0x2582,
        0x81: 0x2583,
        0x201A: 0x2584,  # raw: 0x82
        0x0192: 0x2585,  # raw: 0x83
        0x201E: 0x2586,  # raw: 0x84
        0x2026: 0x2587,  # raw: 0x85
        0x2020: 0x2588,  # raw: 0x86
    }

    def get_LCD(self):
        if self.is_open():
            try:
                Response = self.Telescope.CommandString("ED", False)
            except win32com.client.pywintypes.com_error as e:
                # Sometimes the handbox needs long time for calculations and does not
                # send the LCD contents before the ASCOM driver trows a timeout exception.
                # Here we catch these timeout exceptions.
                print(f'ERROR in get_LCD: {e}')
            #print(f'sendCommandString response: {Response}')
            return Response[1:].translate(self.CharacterTranslationTable)
        return None

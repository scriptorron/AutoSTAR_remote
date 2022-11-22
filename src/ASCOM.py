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

    def sendCommandString(self, cmd):
        if self.is_open():
            try:
                return self.Telescope.CommandString(cmd, False)
            except win32com.client.pywintypes.com_error as e:
                # Sometimes the handbox needs long time for calculations and does not
                # send the LCD contents before the ASCOM driver trows a timeout exception.
                # Here we catch these timeout exceptions.
                print(f'updateLCD: {e}')
        return None

# AutoSTAR_remote
This is a GUI to remote control (using ASCOM or serial interface) the Meade AutoSTAR #497 handheld.

![screenshot](AutoSTAR_remote_V1.0.png)

Press [SHIFT] when clicking on "ENTER", "MODE" or "GO TO" to generate a long key press.

You can change the serial port parameters when connecting with UART. Default parameters for the MEADE AutoSTAR #497 are:
- Speed: 9600 baud
- 8 data bits
- 1 stop bit
- no parity
- no flow control

When connecting with the serial port you have the option to set the time and date of the AutoSTAR to the computer clock. This feature is not fully tested. Especially the daylight saving may be wrong. Please check the AutoSTAR settings if you see strange errors when doing GOTO to an object.

The compiled binary just needs to be unpacked. No installation and no Python is needed. ASCOM driver https://bitbucket.org/cjdskunkworks/meadeautostar497 must be installed and off course you need to connect your #497 AutoSTAR with your computer.

For running the Python source code you need the following packages:
- PyQt5
- pyserial
- win32com when using ASCOM on Windows

The Python source code runs also on Raspberry Pi (Astroberry). 

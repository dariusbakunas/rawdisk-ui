import logging
import binascii
import mmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem, QDesktopWidget
from gui.generated.ui_main_window import Ui_MainWindow
from gui.logger_console import LoggerConsole
from rawdisk.session import Session
from gui.hex_edit import HexEdit

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.hex_edit = HexEdit(self.centralwidget, addr_section=True)
        self.hex_edit.setObjectName("hexEdit")
        self.gridLayout.addWidget(self.hex_edit, 1, 0, 1, 1)
        self.center()
        self.actionOpen.triggered.connect(self.open)

    def open(self):
        filename, _ = QFileDialog.getOpenFileName(
            directory='/Users/darius/Programming/rawdisk/sample_images',
            parent=self,
            caption='Open Disk Image',
            filter='All Supported Formats (*.bin *.img *.vhd);;Virtual Hard Disk (*.vhd);;Disk Image (*.img);;Binary File (*.bin)'
        )
        if filename:
            self.hex_edit.load(filename)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
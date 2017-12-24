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

        self.hex_edit = HexEdit(self.centralwidget)
        self.hex_edit.setObjectName("hexEdit")
        self.gridLayout.addWidget(self.hex_edit, 1, 0, 1, 1)

        # self.hexEdit.insertPlainText('eb 52 90 4e 54 46 53 20 20 20 20 00 02 08 00 00 ')
        # self.hexEdit.insertPlainText('00 00 00 00 00 f8 00 00 3f 00 ff 00 80 00 00 00 ')
        # self.hexEdit.insertPlainText('00 00 00 00 80 00 80 00 ff 37 00 00 00 00 00 00 ')
        # logger = LoggerConsole(self.loggingTextBox)
        # logger.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        # logging.getLogger().addHandler(logger)
        # logging.getLogger().setLevel(logging.INFO)

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

            # str = ''.join('{:02x} '.format(x) for x in chunk)
            # self.hexEdit.insertPlainText(str)
            # session = Session(filename=filename)

            # for volume in session.volumes:
            #     item = QListWidgetItem('{}'.format(volume))
            #     self.volumeList.addItem(item)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
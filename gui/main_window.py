import logging
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QListWidgetItem, QDesktopWidget
from gui.generated.ui_main_window import Ui_MainWindow
from gui.logger_console import LoggerConsole
from rawdisk.session import Session


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.setupUi(self)

        logger = LoggerConsole(self.loggingTextBox)
        logger.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(logger)
        logging.getLogger().setLevel(logging.INFO)

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
            session = Session(filename=filename)

            for volume in session.volumes:
                item = QListWidgetItem('{}'.format(volume))
                self.volumeList.addItem(item)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
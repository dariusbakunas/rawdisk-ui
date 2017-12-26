from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDesktopWidget
from gui.generated.ui_main_window import Ui_MainWindow
from gui.hex_edit import HexEdit

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.hex_edit = HexEdit(self.centralwidget, addr_section=True, ascii_section=True)
        self.hex_edit.setObjectName("hexEdit")
        self.gridLayout.addWidget(self.hex_edit, 1, 0, 1, 1)
        self.center()
        self.actionOpen.triggered.connect(self.open)
        self.hex_edit.offset_changed.connect(self.update_offset)

        self.offset = 0
        self.filename = None

    def update_offset(self, offset):
        self.offset = offset
        self.update_status_bar()

    def update_status_bar(self):
        self.statusbar.showMessage('Filename: {}, offset: {:X}'.format(self.filename, self.offset))

    def open(self):
        formats = [
            'All Disk Formats (*.bin *.img *.vhd)',
            'Virtual Hard Disk (*.vhd)',
            'Disk Image (*.img)',
            'Binary File (*.bin)',
            'All Files (*.*)',
        ]

        self.filename, _ = QFileDialog.getOpenFileName(
            directory='/Users/darius/Programming/rawdisk/sample_images',
            parent=self,
            caption='Open Disk Image',
            filter=';;'.join(formats)
        )
        if self.filename:
            self.hex_edit.load(self.filename)

        self.update_status_bar()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDesktopWidget, QMenuBar
from gui.generated.ui_main_window import Ui_MainWindow
from gui.hex_edit import HexEdit

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.center()
        self.actionOpen.triggered.connect(self.open)
        self.tabs.tabCloseRequested.connect(self.remove_tab)

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

        filename, _ = QFileDialog.getOpenFileName(
            directory='/Users/darius/Programming/rawdisk/sample_images',
            parent=self,
            caption='Open Disk Image',
            filter=';;'.join(formats)
        )

        if filename:
            tab = HexEdit(self.tabs, addr_section=True, ascii_section=True)
            tab.load(filename)
            self.tabs.addTab(tab, filename)

    def remove_tab(self, index):
        widget = self.tabs.widget(index)
        if widget is not None:
            widget.deleteLater()
        self.tabs.removeTab(index)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
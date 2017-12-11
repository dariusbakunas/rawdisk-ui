#!/usr/bin/env python
# coding=utf-8

import sys
from PyQt5 import QtWidgets
from gui.main_window import MainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

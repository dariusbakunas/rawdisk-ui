#!/usr/bin/env python
# coding=utf-8

import sys
import logging
from util.logging import setup_logging
from PyQt5 import QtWidgets
from gui.main_window import MainWindow


if __name__ == '__main__':
    setup_logging(log_level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # deals with the PyQt specific problem in OS-X, that an application window
    # is not automatically brought to the front on launch
    window.raise_()
    sys.exit(app.exec_())

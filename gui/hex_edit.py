# coding=utf-8

import math
import mmap
import os
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QAbstractScrollArea
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QFontDatabase, \
    QFontMetrics


class HexEdit(QAbstractScrollArea):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__mmap = None
        self.__max_bytes = 1024
        self.__file_size = 0
        self.__offset = 0
        self.initUI()

    def initUI(self):
        self.setMinimumSize(1, 30)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixed_font.setPointSize(12)
        self.setFont(fixed_font)
        self.verticalScrollBar().setValue(0)

    def setFont(self, font):
        super().setFont(font)
        self.__font_metrics = QFontMetrics(font)
        self.__char_width = self.__font_metrics.width('B')
        self.__char_height = self.__font_metrics.height()

    def paintEvent(self, e):
        qp = QPainter(self.viewport())
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def closeEvent(self, QCloseEvent):
        if self.__mmap:
            self.__mmap.close()
            self.__file.close()

    def load(self, filename):
        self.__file_size = os.path.getsize(filename)
        self.__file = open(filename, 'rb')

        self.reload_mmap()

    def reload_mmap(self):
        if self.__mmap:
            self.__mmap.close()

        length = self.__max_bytes if self.__max_bytes < self.__file_size else self.__file_size
        self.__mmap = mmap.mmap(self.__file.fileno(), length=length, access=mmap.ACCESS_READ, offset=self.__offset)
        self.viewport().update()

    @property
    def bytes_per_line(self):
        return self.__bytes_per_line

    def update_bytes_per_line(self):
        viewport_width = self.viewport().width()
        num_bytes = int((viewport_width / self.__char_width) / 3)
        width = self.__font_metrics.width('AA ' * num_bytes) - self.__font_metrics.width(' ')
        self.__bytes_per_line = num_bytes - 1 if width > viewport_width else num_bytes

    def update_max_bytes(self):
        viewport_height = self.viewport().height()
        lines = viewport_height // self.__char_height
        total_bytes = lines * self.__bytes_per_line
        chunks = math.ceil(total_bytes / 1024)
        max_bytes = 1024 * chunks
        if self.__max_bytes != max_bytes:
            self.__max_bytes = max_bytes
            self.reload_mmap()

    def resizeEvent(self, QResizeEvent):
        self.update_bytes_per_line()
        self.update_max_bytes()

    def drawWidget(self, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(255, 255, 255))

        if self.__mmap:
            rows = math.ceil(self.__max_bytes / self.bytes_per_line)
            for row in range(int(rows)):
                y_pos = (row + 1) * self.__char_height
                offset = row * self.__bytes_per_line
                chunk = self.__mmap[offset:offset + self.__bytes_per_line]
                str = ''.join('{:02x} '.format(x) for x in chunk)
                qp.drawText(0, y_pos, str)

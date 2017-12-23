# coding=utf-8

import math
import mmap
import os
from PyQt5.QtWidgets import QAbstractScrollArea
from PyQt5.QtGui import QPainter, QColor, QFontDatabase, \
    QFontMetrics


CHUNK_SIZE = 1024

class HexEdit(QAbstractScrollArea):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__mmap = None
        self.__max_bytes = CHUNK_SIZE
        self.__rows_shown = 0
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
        self.update_metrics()

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
        self.__mmap = mmap.mmap(
            fileno=self.__file.fileno(),
            length=length,
            access=mmap.ACCESS_READ,
            offset=self.__offset)
        self.viewport().update()

    def get_bytes_per_row(self, font_metrics, row_width):
        char_width = font_metrics.width('B')
        num_bytes = int((row_width / char_width) / 3)

        # calculate width if we print that many bytes and adjust if necessary
        width = font_metrics.width('AA ' * num_bytes) - font_metrics.width(' ')
        return num_bytes - 1 if width > row_width else num_bytes

    def get_max_bytes(self, total_rows, bytes_per_row):
        total_bytes = total_rows * bytes_per_row
        return math.ceil(total_bytes / CHUNK_SIZE) * CHUNK_SIZE

    def update_metrics(self):
        viewport_width = self.viewport().width()
        viewport_height = self.viewport().height()
        self.__bytes_per_row = self.get_bytes_per_row(
            font_metrics=self.__font_metrics,
            row_width=viewport_width)
        self.__rows_shown = viewport_height // self.__font_metrics.height()
        max_bytes = self.get_max_bytes(
            total_rows=self.__rows_shown,
            bytes_per_row=self.__bytes_per_row)

        if self.__max_bytes != max_bytes:
            self.__max_bytes = max_bytes
            self.reload_mmap()


    def resizeEvent(self, QResizeEvent):
        self.update_metrics()

    def drawWidget(self, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(255, 255, 255))

        if self.__mmap:
            for row in range(int(self.__rows_shown)):
                y_pos = (row + 1) * self.__font_metrics.height()
                offset = row * self.__bytes_per_row
                chunk = self.__mmap[offset:offset + self.__bytes_per_row]
                str = ''.join('{:02x} '.format(x) for x in chunk)
                qp.drawText(0, y_pos, str)

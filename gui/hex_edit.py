# coding=utf-8

import math
import logging
from util.mem_buffer import MemBuffer
from PyQt5.QtWidgets import QAbstractScrollArea
from PyQt5.QtGui import QPainter, QColor, QFontDatabase, \
    QFontMetrics

logger = logging.getLogger(__name__)

class HexEdit(QAbstractScrollArea):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__buffer = None
        self.__rows_shown = 0
        self.__total_rows = 0
        self.__addr_width = 0
        self.initUI()

    def initUI(self):
        self.setMinimumSize(1, 30)
        font_db = QFontDatabase()
        fixed_font = font_db.systemFont(QFontDatabase.FixedFont)
        fixed_font.setPointSize(12)
        self.setFont(fixed_font)
        self.verticalScrollBar().valueChanged.connect(self.updateScroll)

    def updateScroll(self, value):
        self.__buffer.offset = value * self.__bytes_per_row
        self.viewport().update()

    def wheelEvent(self, event):
        num_pixels_pt = event.pixelDelta()

        # TODO: handle degrees if pixels not avail
        num_degress = event.angleDelta() / 8

        if num_pixels_pt is not None:
            y_diff = num_pixels_pt.y()
            current_row = self.verticalScrollBar().value()
            row = current_row - y_diff if y_diff < current_row else 0
            row = self.__total_rows if row > self.__total_rows else row
            self.verticalScrollBar().setValue(row)

    def setFont(self, font):
        super().setFont(font)
        self.__font_metrics = QFontMetrics(font)
        self.update_metrics()

    def paintEvent(self, e):
        qp = QPainter(self.viewport())
        # qp.begin(self)
        self.drawWidget(qp)
        # qp.end()

    def closeEvent(self, QCloseEvent):
        if self.__buffer:
            self.__buffer.close()

    def load(self, filename):
        self.__buffer = MemBuffer(
            filename,
            min_size=self.__rows_shown * self.__bytes_per_row)

        self.__addr_width = self.__font_metrics.width(
            ' {:X}  '.format(self.__buffer.size))

        self.verticalScrollBar().setValue(0)
        self.update_total_rows()
        self.viewport().update()

    def set_offset(self, offset):
        self.__buffer.offset = offset
        self.viewport().update()

    def update_total_rows(self):
        self.__total_rows = math.ceil(
            self.__buffer.size / self.__bytes_per_row)

        self.verticalScrollBar().setRange(0, self.__total_rows - self.__rows_shown)
        self.verticalScrollBar().setPageStep(self.__rows_shown)

    def get_bytes_per_row(self, font_metrics, row_width):
        char_width = font_metrics.width('B')
        num_bytes = int((row_width / char_width) / 3)

        # calculate width if we print that many bytes and adjust if necessary
        width = font_metrics.width('AA ' * num_bytes) - font_metrics.width(' ')
        return num_bytes - 1 if width > row_width else num_bytes

    def update_metrics(self):
        viewport_width = self.viewport().width() - self.__addr_width
        viewport_height = self.viewport().height()
        self.__bytes_per_row = self.get_bytes_per_row(
            font_metrics=self.__font_metrics,
            row_width=viewport_width)
        self.__rows_shown = viewport_height // self.__font_metrics.height()

        if self.__buffer:
            self.__buffer.min_size = self.__rows_shown * self.__bytes_per_row
            offset = self.verticalScrollBar().value() * self.__bytes_per_row
            self.__buffer.offset = self.__buffer.size if offset > self.__buffer.size else offset
            self.update_total_rows()

    def resizeEvent(self, QResizeEvent):
        self.update_metrics()

    def drawWidget(self, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(255, 255, 255))

        if self.__buffer:
            remaining_rows = math.ceil(self.__buffer.remaining_bytes / self.__bytes_per_row)
            padding = len('{:X}'.format(self.__buffer.size))

            for row in range(min(int(self.__rows_shown), remaining_rows)):
                y_pos = (row + 1) * self.__font_metrics.height()
                offset = row * self.__bytes_per_row + self.__buffer.offset
                row_bytes = self.__buffer[offset:offset + self.__bytes_per_row]
                addr_str = '{:X}'.format(offset)
                bytes_str = ''.join('{:02X} '.format(x) for x in row_bytes)
                qp.drawText(0, y_pos, ' ' + addr_str.rjust(padding, '0'))
                qp.drawText(self.__addr_width, y_pos, bytes_str)

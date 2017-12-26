# coding=utf-8

import math
import logging
from util.mem_buffer import MemBuffer
from PyQt5.QtWidgets import QAbstractScrollArea
from PyQt5.QtGui import QPainter, QColor, QFontDatabase, QFontMetrics
from PyQt5.QtCore import pyqtSignal

logger = logging.getLogger(__name__)

class HexEdit(QAbstractScrollArea):
    # signals
    offset_changed = pyqtSignal(int, name='offsetChanged')

    def __init__(self, parent = None, addr_section = True, ascii_section = True):
        super().__init__(parent)
        self.__buffer = None
        self.__rows_shown = 0
        self.__total_rows = 0
        self.__addr_width = 100
        self.__ascii_width = 0
        self.__show_addr_section = addr_section
        self.__show_ascii_section = ascii_section

        self.__addr_bg_color = QColor(188, 188, 188)
        self.__addr_fg_color = QColor(75, 75, 75)
        self.__main_fg_color = QColor(0, 0, 0)

        self.initUI()

    def initUI(self):
        self.setMinimumSize(300, 400)
        font_db = QFontDatabase()
        fixed_font = font_db.systemFont(QFontDatabase.FixedFont)
        fixed_font.setPointSize(12)
        self.setFont(fixed_font)
        self.verticalScrollBar().valueChanged.connect(self.updateScroll)

    def updateScroll(self, value):
        offset = value * self.__bytes_per_row
        self.set_offset(offset)

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

        if self.__show_addr_section:
            self.__addr_width = self.__font_metrics.width(
                ' {:X} '.format(self.__buffer.size))

        self.verticalScrollBar().setValue(0)
        self.update_metrics()
        self.viewport().update()

    def set_offset(self, offset):
        self.__buffer.offset = offset
        self.offset_changed.emit(offset)
        self.viewport().update()

    def update_total_rows(self):
        self.__total_rows = math.ceil(
            self.__buffer.size / self.__bytes_per_row)

        self.verticalScrollBar().setRange(0, self.__total_rows - self.__rows_shown)
        self.verticalScrollBar().setPageStep(self.__rows_shown)

    def get_bytes_per_row(self, font_metrics, row_width, ascii_section=True):
        """Return number of bytes that can fit in one row, including ascii section"""
        char_width = font_metrics.width('B')

        if ascii_section:
            num_bytes = int(math.floor(((row_width / char_width) - 4) / 4))
            width = font_metrics.width('AA ' * num_bytes) + font_metrics.width(
                'A' * num_bytes) + font_metrics.width('SS')
        else:
            num_bytes = int(math.floor(((row_width / char_width) - 1) / 3))
            width = font_metrics.width('AA ' * num_bytes) + font_metrics.width('S')

        return num_bytes - 1 if width > row_width else num_bytes

    def update_metrics(self):
        viewport_width = self.viewport().width()
        viewport_height = self.viewport().height()
        self.__bytes_per_row = self.get_bytes_per_row(
            font_metrics=self.__font_metrics,
            row_width=viewport_width - self.__addr_width,
            ascii_section=self.__show_ascii_section
        )
        self.__rows_shown = viewport_height // self.__font_metrics.height()

        if self.__buffer:
            self.__buffer.min_size = self.__rows_shown * self.__bytes_per_row
            offset = self.verticalScrollBar().value() * self.__bytes_per_row
            offset = self.__buffer.size if offset > self.__buffer.size else offset
            self.__buffer.offset = offset
            self.offset_changed.emit(offset)
            self.update_total_rows()

    def resizeEvent(self, QResizeEvent):
        self.update_metrics()

    def decode_byte(self, byte):
        x = int.from_bytes([byte], byteorder='big')
        if (x > 32 and x < 126):
            return chr(x)
        else:
            return '.'

    def render_ascii_line(self, x, y, painter, bytes):
        ascii_str = ''.join([self.decode_byte(x) for x in bytes])
        painter.drawText(x, y, '{} '.format(ascii_str))

    def render_addr_line(self, x, y, painter, address, padding):
        painter.setPen(self.__addr_fg_color)
        addr_str = '{:X}'.format(address)
        painter.drawText(x, y, ' ' + addr_str.rjust(padding, '0'))

    def render_byte_line(self, x, y, painter, bytes):
        painter.setPen(self.__main_fg_color)
        bytes_str = ' '.join('{:02X}'.format(x) for x in bytes)
        painter.drawText(x, y, ' ' + bytes_str + ' ')

    def render_addr_section(self, width, height, painter):
        painter.setBrush(self.__addr_bg_color)
        painter.setPen(self.__addr_bg_color)
        painter.drawRect(0, 0, width, height)

    def drawWidget(self, qp):
        self.render_addr_section(
            width=self.__addr_width if self.__show_addr_section else 100,
            height=self.viewport().height(),
            painter=qp
        )

        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(255, 255, 255))

        if self.__buffer:
            remaining_rows = math.ceil(self.__buffer.remaining_bytes / self.__bytes_per_row)
            addr_padding = len('{:X}'.format(self.__buffer.size))

            for row in range(min(self.__rows_shown, remaining_rows)):
                row_y = (row + 1) * self.__font_metrics.height()
                offset = row * self.__bytes_per_row + self.__buffer.offset
                row_bytes = self.__buffer[offset:offset + self.__bytes_per_row]

                if self.__show_addr_section:
                    self.render_addr_line(
                        x=0,
                        y=row_y,
                        painter=qp,
                        address=offset,
                        padding=addr_padding)

                bytes_x = self.__addr_width if self.__show_addr_section else 0

                self.render_byte_line(
                    x=bytes_x,
                    y=row_y,
                    painter=qp,
                    bytes=row_bytes)

                if self.__show_ascii_section:
                    bytes_width = self.__font_metrics.width(' ' + 'AAA' * self.__bytes_per_row + ' ')
                    self.render_ascii_line(
                        x=bytes_x + bytes_width,
                        y=row_y,
                        painter=qp,
                        bytes=row_bytes)

# coding=utf-8

import os
import mmap
import logging

logger = logging.getLogger(__name__)


class MemBuffer():
    def __init__(self, filename, min_size):
        self.__file_size = os.path.getsize(filename)
        self.__file = open(filename, 'rb')
        self.__start_offset = 0
        self.__end_offset = 0
        self.__current_offset = 0
        self.__min_size = min_size
        self.__mmap = None
        self.load_mmap()

    def __getitem__(self, item):
        # adjust all offsets based on currently loaded mmap offset
        adjusted_slice = slice(
            item.start - self.__start_offset,
            item.stop - self.__start_offset,
            item.step)
        return self.__mmap[adjusted_slice]

    def __len__(self):
        return self.__end_offset - self.__start_offset

    @property
    def offset(self):
        return self.__current_offset

    @offset.setter
    def offset(self, value):
        self.__current_offset = value

        if self.need_reload():
            self.load_mmap()

    def need_reload(self):
        if self.__end_offset == self.__file_size and self.__start_offset == 0:
            return False

        return (self.__end_offset - self.__current_offset <= self.__min_size) or \
               (self.__start_offset != 0 and (self.__current_offset - self.__start_offset <= self.__min_size))

    @property
    def min_size(self):
        return self.__min_size

    @min_size.setter
    def min_size(self, value):
        self.__min_size = value

    @property
    def start_offset(self):
        return self.__start_offset

    @property
    def end_offset(self):
        return self.__end_offset

    @property
    def size(self):
        return self.__file_size

    def close(self):
        if self.__mmap:
            self.__mmap.close()

        if self.__file:
            self.__file.close()

    @property
    def remaining_bytes(self):
        return self.__file_size - self.__current_offset

    def load_mmap(self):
        if self.__mmap:
            self.__mmap.close()

        adjusted_offset = self.__current_offset - self.__current_offset % mmap.ALLOCATIONGRANULARITY

        # total window size is 4 * mmap.ALLOCATIONGRANULARITY
        self.__start_offset = max(adjusted_offset - 4 * mmap.ALLOCATIONGRANULARITY, 0)
        self.__end_offset = min(adjusted_offset + 4 * mmap.ALLOCATIONGRANULARITY, self.__file_size)

        logger.debug('loading mmap - start: {}, end: {}, current offset: {}'
                     .format(self.start_offset, self.end_offset, self.offset))

        self.__mmap = mmap.mmap(
            fileno=self.__file.fileno(),
            length=self.end_offset - self.start_offset,
            access=mmap.ACCESS_READ,
            offset=self.start_offset)

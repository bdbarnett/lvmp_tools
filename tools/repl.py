# SPDX-FileCopyrightText: 2023 Brad Barnett, 2021 Jan Staal, 2017 Boochow
#
# SPDX-License-Identifier: MIT
#
# Based on work by boochow at https://github.com/boochow/FBConsole
# Based on work by JohnieBraaf at https://github.com/JohnieBraaf/Boat-Controller-Micropython-LVGL

import io
import os


class REPL(io.IOBase):
    def __init__(self, console):
        self.console = console
        self.buf = TextBuffer(1000, 15, 1)
        try:
           os.dupterm(self)
        except AttributeError:
            self.console.add_text("AttributeError:  Unable to start REPL.  Your micropython was compiled without os.dupterm enabled.")
            return
        self.timer = self.create_timer()

    @micropython.native
    def readinto(self, buf, nbytes=0):
        return None
    
    @micropython.native
    def write(self, buf):
        i = 0
        while i < len(buf):
            c = buf[i]
            if c == "\n":
                i +=1
                self.buf.put(c)
            elif c == 0x1B:  # remove escape chars
                i += 1
                while chr(buf[i]) in "[;0123456789":
                    i += 1
                    c = buf[i]
                    if c != 0x4b and c != 0x4:
                        self.console.add_text(hex(c))
            else:
                if c == 0x8:  # backspace
                    self.console.del_char()
                elif c != 0xA:  # normal character
                    self.buf.put(c)
            i += 1

        # print directly to console
        if self.buf.dirty_read:
            self.console.set_text(self.buf.get_text(True))
            self.buf.read_text()  # flag all as read
        self.console.add_text(self.buf.read_text())

        return len(buf)

    def repl_cb(self):
        if self.buf.dirty_read:
            self.console.set_text(self.buf.get_text(True))
            self.buf.read_text()  # flag all as read
        self.console.add_text(self.buf.read_text())

    def create_timer(self):
        raise NotImplementedError(
            "Method 'create_timer' must defined in a sublass of REPL"
        )


class Lv_Repl(REPL):
    def __init__(self, console):
        super().__init__(console)

    def create_timer(self):
        import lvgl as lv

        timer = lv.timer_create_basic()
        timer.set_period(500)
        timer.set_repeat_count(-1)
        timer.set_cb(lambda e: self.repl_cb())
        return timer

    def _del(self):
        try:
            os.dupterm(None)
        except AttributeError:
            return
        self.timer._del()


#
# RingBuffer
#
# - size: number of bytes allocated to text
#
class RingBuffer:
    def __init__(self, size):
        self.size = size + 1
        self.data = bytearray(self.size)
        self.index_put = 0
        self.index_get = 0
        self.count = 0

    @micropython.native
    def any(self):
        if self.index_get != self.index_put:
            return True
        return False

    @micropython.native
    def put(self, value):
        next_index = (self.index_put + 1) % self.size

        if self.index_get != next_index:
            self.data[self.index_put] = value
            self.index_put = next_index
            self.count += 1
            return value
        else:
            return 0x00  # buffer full

    @micropython.native
    def get(self):
        if self.any():
            value = self.data[self.index_get]
            self.index_get = (self.index_get + 1) % self.size
            self.count -= 1
            return value
        else:
            return 0x00  # buffer empty


#
# TextBuffer
#
# - size: number of bytes allocated to text
# - lines_max: maximum number of lines to keep in buffer (0xd new line delimited)
# - lines_trim: number of lines to trim if lines_max is reached
#
# Adds index_read to the ringbuffer, and dirty_read to flag if the reader is in sync
# get_text() resets the dirty_read flag, after which read_text() can be used for subsequent reads
#
class TextBuffer(RingBuffer):
    def __init__(self, size, lines_max, lines_trim):
        super().__init__(size)
        self.lines_max = lines_max
        self.lines_trim = lines_trim
        self.lines_count = 0
        self.index_read = 0
        self.dirty_read = False

    @micropython.native
    def put(self, value):
        if self.index_get == (self.index_put + 1) % self.size:  # buffer full,
            self.get_line()  # pop line from buffer

        super().put(value)

        if value == 0xD:
            self.lines_count += 1
            if self.lines_count > self.lines_max:  # too many lines
                self.get_line(self.lines_trim)  # pop number of lines from buffer

    @micropython.native
    def get_line(self, num=1, peek=False):
        old_index = self.index_get  # save index
        old_count = self.count  # save count
        ret = ""
        for i in range(num):
            while self.any():
                c = self.get()
                if c == 0xD:
                    break
                ret += str(chr(c)) + str(hex(c))
        if peek:
            self.index_get = old_index  # reset index
            self.count = old_count  # reset count
        else:
            self.lines_count -= num
        self.dirty_read = True
        return ret

    @micropython.native
    def get_text(self, peek=False):
        old_index = self.index_get  # save index
        old_count = self.count  # save count
        ret = ""
        while self.any():
            ret += str(chr(self.get()))
        if peek:
            self.index_get = old_index  # reset index
            self.count = old_count  # reset count
        self.dirty_read = False
        return ret

    @micropython.native
    def any_read(self):
        if self.index_read != self.index_put:
            return True
        return False

    @micropython.native
    def read(self):
        if self.any_read():
            value = self.data[self.index_read]
            self.index_read = (self.index_read + 1) % self.size
            return value
        else:
            return None  # buffer empty

    @micropython.native
    def read_text(self):
        ret = ""
        while self.any_read():
            ret += str(chr(self.read()))
        return ret

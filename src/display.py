from uQR import QRCode
import epaper1in54
from machine import SPI
from machine import Pin
import gc


black = 0
white = 1
w = 200
h = 200
x = 0
y = 0


class PaperDisplay2:
    def __init__(self):
        spi = SPI(baudrate=100000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(16))
        cs = Pin(15, Pin.OUT)
        dc = Pin(32, Pin.OUT)
        rst = Pin(2, Pin.OUT)
        busy = Pin(0, Pin.OUT)
        self.display = epaper1in54.EPD(spi, cs, dc, rst, busy)
        self.display.init()
        self.color = black
        self.background = white
        self.fb, self.buf = self.init_fb()
        self.clear(show=True)

    def set_color(self, color):
        self.color = color
        if color == white:
            self.background = black
        else:
            self.background = white

    def init_fb(self):
        import framebuf
        buf = bytearray(w * h // 8)
        fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
        fb.fill(self.background)
        return fb, buf

    def clear(self, show=False):
        self.fb, self.buf = self.init_fb()
        if show:
            self.show()

    def show(self):
        self.display.set_frame_memory(self.buf, x, y, w, h)
        self.display.display_frame()

    def set_px_scaled(self, x, y, scale):
        pos_x = x * scale
        pos_y = y * scale
        for xx in range(pos_x, pos_x + scale):
            for yy in range(pos_y, pos_y + scale):
                self.fb.pixel(xx, yy, self.color)

    def set_matrix(self, matrix):
        matrix_w = len(matrix)
        matrix_h = len(matrix[0])
        scale = int(min(w / matrix_w, h / matrix_h))
        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                if matrix[x][y]:
                    self.set_px_scaled(x, y, scale=scale)


def gen_qr(text):
    qr = QRCode()
    qr.add_data(text)
    return qr.get_matrix()


def nearest_neighbour(dim_x, dim_y, ndim_x, ndim_y, pos_x, pos_y):
    neighbour_x = round(pos_x/(float(ndim_x)/dim_x))
    neighbour_y = round(pos_y/(float(ndim_y)/dim_y))
    return neighbour_x, neighbour_y


def upscale(matrix):
    scale = 100
    new_matrix = []
    for _ in range(scale):
        empty_line = []
        for i in range(scale):
            if i % 20:
                gc.collect()
            empty_line.append(False)
        new_matrix.append(empty_line)
        gc.collect()
    for x in range(scale):
        for y in range(scale):
            neigh_x, neigh_y = nearest_neighbour(len(matrix), len(matrix[0]), scale, scale, x, y)
            new_matrix[x][y] = matrix[neigh_x][neigh_y]
            if y % 20:
                gc.collect()
    return new_matrix







import imageio
import numpy as np
import pyqtgraph.opengl as gl
from PIL import Image as PILImage
from OpenGL.GL import GL_RGBA
from pyqtgraph import mkQApp
from pyqtgraph.Qt import QtCore


def _create_window(w, h, res_w=1920, res_h=1080, title=None, cam_dist=50, cam_elev=2, cam_azim=45):
    win_x = res_w // 2 - w // 2
    win_y = res_h // 2 - h // 2
    win = gl.GLViewWidget()
    win.setGeometry(win_x, win_y, w, h)
    win.setWindowTitle(title or '')
    win.setCameraPosition(distance=cam_dist, elevation=cam_elev, azimuth=cam_azim)
    return win


class FrameBuffer:

    def __init__(self, buf):
        self.buf = buf.copy()

    def to_pil(self, i=0, mode='RGB'):
        arr = self.buf[i].copy()[:, :, :-1]
        return PILImage.fromarray(arr, mode)

    def show(self, i=0, mode='RGB'):
        img = self.to_pil(i=i, mode=mode)
        img.show()

    def save(self, fp, i=0, mode='RGB'):
        img = self.to_pil(i=i, mode=mode)
        img.save(fp)

    def to_gif(self, fp, fps=30):
        imageio.mimwrite(fp, self.buf.copy(), fps=fps)


class Scene:

    def __init__(self, width, height, window_params=None):
        self.width = width
        self.height = height
        window_params = window_params or {}
        window_params = window_params.copy()
        window_params.pop('w', None)
        window_params.pop('h', None)
        self.window_params = window_params

        self.qt_app = mkQApp()
        self.win = _create_window(w=self.width, h=self.height, **self.window_params)
        self._current_item = None

    def _exec(self):
        self.qt_app.exec_()

    def _set_shape(self, shape):
        item = shape.gl_item
        try:
            self.win.removeItem(item)
        except ValueError:
            pass
        self.win.addItem(item)

    def _render_win(self):
        self.win.show()
        self._exec()

    def _render_img(self, size, fmt=GL_RGBA):
        return self.win.renderToArray(size, format=fmt).transpose((1, 0, 2))

    def render(self, shape, size, fmt=GL_RGBA):
        self._set_shape(shape)
        shape.frame()
        arr = self._render_img(size=size, fmt=fmt).astype(np.uint8)
        buf = np.expand_dims(arr, 0)
        fb = FrameBuffer(buf=buf)
        return fb

    def animate(self, shape, n_frames, size, fmt=GL_RGBA):
        buf = []
        self._set_shape(shape)
        for _ in range(n_frames):
            shape.frame()
            arr = self._render_img(size=size, fmt=fmt)
            buf.append(arr)
        buf = np.asarray(buf)
        fb = FrameBuffer(buf)
        return fb

    def irender(self, shape):
        self._set_shape(shape)
        shape.frame()
        self._render_win()

    def ianimate(self, shape, fps=30):
        self._set_shape(shape)
        rate = 1000 // fps
        timer = QtCore.QTimer()
        timer.timeout.connect(shape.frame)
        timer.start(rate)
        self._render_win()

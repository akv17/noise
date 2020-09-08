import pyqtgraph.opengl as gl
from pyqtgraph import mkQApp
from pyqtgraph.Qt import QtCore


def _create_window(w, h, res_w=1920, res_h=1080, title=None, cam_dist=50, cam_elev=4):
    win_x = res_w // 2 - w // 2
    win_y = res_h // 2 - h // 2
    win = gl.GLViewWidget()
    win.setGeometry(win_x, win_y, w, h)
    win.setWindowTitle(title or '')
    win.setCameraPosition(distance=cam_dist, elevation=cam_elev)
    return win


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
        shape = shape.gl_item
        try:
            self.win.removeItem(shape)
        except ValueError:
            pass
        self.win.addItem(shape)

    def _render_win(self):
        self.win.show()
        self._exec()

    def render(self, shape):
        self._set_shape(shape)
        shape.frame()
        self._render_win()

    def animate(self, shape, fps=30):
        self._set_shape(shape)
        rate = 1000 // fps
        timer = QtCore.QTimer()
        timer.timeout.connect(shape.frame)
        timer.start(rate)
        self._render_win()

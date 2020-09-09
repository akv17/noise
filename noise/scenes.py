from abc import abstractmethod

import numpy as np
import pyqtgraph.opengl as gl

from .utils import timer
from .noises import DummyNoise, PerlinNoise
from .colors import GRADIENTS, DummyPalette, GradientPalette


@timer
def make_verts(width, height):
    xs = np.repeat(np.arange(width, dtype=np.float64), height).reshape(-1, 1)
    ys = np.tile(np.arange(height, dtype=np.float64), [width]).reshape(-1, 1)
    zs = np.zeros(shape=(width * height,), dtype=np.float64).reshape(-1, 1)
    vx = np.hstack((xs, ys, zs))
    return vx


@timer
def make_faces(width, height):
    """
    A -- B
    |    |
    D -- C
    tri faces starting from vert A:
        fc0: A-B-C; AB->AC->BC
        fc1: A-D-C; AD->AC->DC
    """
    def ix(x, y):
        return x * height + y

    fcs = []
    for x in range(width - 1):
        for y in range(height - 1):
            # A-B-C
            fc0 = [ix(x, y), ix(x, y + 1), ix(x + 1, y + 1)]
            fcs.append(fc0)
            # A-D-C
            fc1 = [ix(x, y), ix(x + 1, y), ix(x + 1, y + 1)]
            fcs.append(fc1)

    return np.asarray(fcs, dtype=np.int64)


class BaseScene:

    def __init__(self, width, height, noise=None, palette=None):
        self.width = width
        self.height = height
        self.noise = noise or DummyNoise()
        self.palette = palette or DummyPalette()

    @property
    def dims(self):
        return self.width, self.height

    @property
    def n_verts(self):
        return self.width * self.height

    @property
    @abstractmethod
    def gl_item(self):
        raise NotImplementedError

    @abstractmethod
    def _update_verts(self):
        raise NotImplementedError

    @abstractmethod
    def _update_colors(self):
        raise NotImplementedError

    @timer
    def frame(self):
        self._update_verts()
        self._update_colors()


class Grid(BaseScene):

    def __init__(self, width, height, draw_edges=True, noise=None, palette=None):
        super().__init__(width=width, height=height, noise=noise, palette=palette)
        self.draw_edges = draw_edges

        self.verts = make_verts(width=self.width, height=self.height)
        self.faces = make_faces(width=self.width, height=self.height)
        self.vert_colors = np.zeros((len(self.verts), 4), dtype=np.float64)

        self._gl_mesh_item = gl.GLMeshItem(drawEdges=draw_edges)
        self._gl_mesh_data = gl.MeshData(vertexes=self.verts, faces=self.faces, vertexColors=self.vert_colors)
        self._gl_mesh_item.setMeshData(meshdata=self._gl_mesh_data)

    @property
    def n_faces(self):
        return (self.width - 1) * (self.height - 1) * 4

    @property
    def gl_item(self):
        return self._gl_mesh_item

    def _update_verts(self):
        self.verts = self.noise.apply(self.verts)
        self._gl_mesh_data.setVertexes(self.verts)
        self._gl_mesh_item.setMeshData(meshdata=self._gl_mesh_data)

    def _update_colors(self):
        colors = self.palette.apply(self.verts)
        self._gl_mesh_data.setVertexColors(colors)
        self._gl_mesh_item.setMeshData(meshdata=self._gl_mesh_data)


class Water(Grid):

    def __init__(self, width, height, draw_edges=True, speed=0.05, scale=0.2):
        super().__init__(width=width, height=height, draw_edges=draw_edges)
        self.speed = speed
        self.scale = scale
        self.noise = PerlinNoise(speed=self.speed, scale=self.scale)
        self.palette = GradientPalette(*GRADIENTS.WATER)

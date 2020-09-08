import numpy as np
import pyqtgraph.opengl as gl
from opensimplex import OpenSimplex

from .utils import timer

PERLIN_NOISE = OpenSimplex().noise2d


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


class Grid:

    def __init__(self, width, height, draw_edges=True):
        self.width = width
        self.height = height

        self.verts = make_verts(width=self.width, height=self.height)
        self.faces = make_faces(width=self.width, height=self.height)
        self.vert_colors = np.zeros((len(self.verts), 4), dtype=np.float64)

        self._gl_mesh_item = gl.GLMeshItem(drawEdges=draw_edges)
        self._gl_mesh_data = gl.MeshData(vertexes=self.verts, faces=self.faces, vertexColors=self.vert_colors)
        self._gl_mesh_item.setMeshData(meshdata=self._gl_mesh_data)

    @property
    def dims(self):
        return self.width, self.height

    @property
    def n_verts(self):
        return self.width * self.height

    @property
    def n_faces(self):
        return (self.width - 1) * (self.height - 1) * 4

    @property
    def gl_item(self):
        return self._gl_mesh_item

    def _update_z(self):
        self.noise = np.roll(self.noise, 1)
        self.verts[:, -1] = self.noise
        self._gl_mesh_data.setVertexes(self.verts)
        self._gl_mesh_item.setMeshData(meshdata=self._gl_mesh_data)

    def _update_colors(self):
        pass

    @timer
    def frame(self):
        self._update_z()
        self._update_colors()


class PerlinGrid(Grid):

    def __init__(self, width, height, draw_edges=True, speed=0.1, scale=0.2):
        super().__init__(width=width, height=height, draw_edges=draw_edges)
        self.speed = speed
        self.scale = scale
        self._offset = 0

    def _compute_vertex_noise(self, vertex):
        x, y, _ = vertex
        z = PERLIN_NOISE(x * self.scale + self._offset, y * self.scale + self._offset)
        return [x, y, z]

    def _update_z(self):
        self.verts = np.apply_along_axis(self._compute_vertex_noise, 1, self.verts)
        self._gl_mesh_data.setVertexes(self.verts)
        self._gl_mesh_item.setMeshData(meshdata=self._gl_mesh_data)
        self._offset -= self.speed

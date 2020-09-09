from abc import abstractmethod

import numpy as np
from opensimplex import OpenSimplex

_PERLIN_NOISE = OpenSimplex().noise2d


class BaseNoise:

    @abstractmethod
    def apply(self, verts):
        raise NotImplementedError


class DummyNoise(BaseNoise):

    def apply(self, verts):
        return verts


class PerlinNoise(BaseNoise):

    def __init__(self, speed=0.1, scale=0.2):
        self.speed = speed
        self.scale = scale
        self._offset = 0

    def _compute_vertex(self, vertex):
        x, y, _ = vertex
        z = _PERLIN_NOISE(x * self.scale + self._offset, y * self.scale + self._offset)
        return [x, y, z]

    def apply(self, verts):
        verts = np.apply_along_axis(self._compute_vertex, 1, verts)
        self._offset -= self.speed
        return verts

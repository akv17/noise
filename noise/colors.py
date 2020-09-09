from abc import abstractmethod

import numpy as np


class GRADIENTS:
    WATER = ((6, 44, 71), (27, 86, 128))


class BasePalette:

    @abstractmethod
    def apply(self, verts):
        raise NotImplementedError


class DummyPalette(BasePalette):

    def apply(self, verts):
        return np.zeros((len(verts), 4), dtype=np.float64)


class GradientPalette(BasePalette):

    def __init__(self, src, dst, axis=2, alpha=0):
        self.src = tuple(v / 255 for v in src)
        self.dst = tuple(v / 255 for v in dst)
        self.axis = axis
        self.alpha = alpha

    def apply(self, verts):
        src_r, src_g, src_b = self.src
        dst_r, dst_g, dst_b = self.dst
        alpha = self.alpha

        verts = verts.copy()
        n_verts = len(verts)
        vals = verts[:, self.axis]
        idxs = np.argsort(vals)
        colors = [None] * n_verts

        for i, idx in enumerate(idxs):
            intens = i / n_verts
            r = src_r + intens * (dst_r - src_r)
            g = src_g + intens * (dst_g - src_g)
            b = src_b + intens * (dst_b - src_b)
            colors[idx] = [r, g, b, alpha]

        return np.asarray(colors)

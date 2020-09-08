from noise.core import Scene
from noise.shapes import PerlinGrid
from noise.colors import GradientPalette

W, H = 1200, 600
GW, GH = 40, 40
scene = Scene(W, H)
palette = GradientPalette(src=(19, 91, 117), dst=(25, 168, 128))
grid = PerlinGrid(GW, GH, palette=palette, draw_edges=True)
scene.animate(shape=grid)

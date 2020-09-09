from noise.core import Scene
from noise.shapes import PerlinGrid
from noise.colors import GradientPalette

W, H = 1200, 600
GW, GH = 100, 100
scene = Scene(width=1200, height=600)
palette = GradientPalette(src=(6, 44, 71), dst=(27, 86, 128))
grid = PerlinGrid(width=100, height=100, palette=palette, draw_edges=True, speed=0.05)
fb = scene.render(shape=grid, size=(1200, 600))
fb.show()

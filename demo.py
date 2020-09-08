from noise.core import Scene
from noise.shapes import PerlinGrid

W, H = 1200, 600
GW, GH = 40, 40
scene = Scene(W, H)
grid = PerlinGrid(GW, GH)
scene.animate(shape=grid)

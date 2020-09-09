from noise.core import Scene
from noise.shapes import Grid
from noise.noises import PerlinNoise
from noise.colors import GradientPalette


scene = Scene(width=1200, height=600)
noise = PerlinNoise(speed=0.05)
palette = GradientPalette(src=(6, 44, 71), dst=(27, 86, 128))
grid = Grid(width=50, height=50, noise=noise, palette=palette, draw_edges=True)
scene.ianimate(grid)

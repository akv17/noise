from noise.core import View
from noise.scenes import Grid
from noise.noises import PerlinNoise
from noise.colors import GradientPalette


view = View(width=1200, height=600)
noise = PerlinNoise(speed=0.05)
palette = GradientPalette(src=(6, 44, 71), dst=(27, 86, 128))
grid = Grid(width=50, height=50, noise=noise, palette=palette, draw_edges=True)
view.ianimate(grid)

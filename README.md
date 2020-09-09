# noise
# Examples
- animate water-like grid.
```
from noise.core import View
from noise.scenes import Water

view = View(width=1200, height=600)
scene = Water(width=50, height=50)
film = view.animate(scene, n_frames=300, size=(1200, 600))
film.to_gif('water.gif')
```
![](examples/water.gif)

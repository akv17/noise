# noise
# Examples
- animate water-like grid.
```
from noise.core import View
from noise.scenes import Water

view = View(width=1200, height=600)
scene = Water(width=50, height=50)
film = view.animate(scene)
film.to_gif('w.gif')
```
![](examples/w.gif)

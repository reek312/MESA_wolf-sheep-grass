# MESA_wolf-sheep-grass

This is my first agent based model(ABM), built while learning MESA.
 
There are 3 agents:
- Grass
- Sheep
- Wolf

They eat each other the way you'd expect: wolf -> sheep -> grass. The simulation runs for a set number of steps and produces the classic Lotka-Volterra style graph.
 
For most of the property understanding and analysis, the dataframe + graph gives good enough visualization, and that's what I used for debugging.
 
There's also an animated visualization (`app.py`) using Mesa's newer Solara framework, if you want to actually watch the agents move around.
 
## Notes from building this ( it's a learning project, so keeping these here)
 
- There are two Wolf classes in the code (one inherited from Sheep, one standalone). Both work fine. I originally used the inherited one, and at some point while debugging I wondered if that was causing issues (it wasn't), so I rewrote a separate standalone Wolf class anyway.
- I underestimated how much tuning it takes to keep the system balanced. It's surprisingly easy for the agents to go extinct (probably because there are 3 species instead of 2).
- Using a strict/constant value for cost works better than a relative one. When reproduction cost was something like 1/2 or 1/3 of the current energy, it didn't work great. Switching to a flat constant cost fixed that (it's also just easier to tune). I noticed the same thing on some EC projects too.
- I haven't tested the age parameter properly yet. I was tweaking every parameter at once trying to find a good balance and a good looking graph, so I set age to max for the moment and forgot to go back and test it properly.
- Even after tuning, the population still goes extinct roughly 10-20% of the time.
- Still not sure how to make the animation move faster.
## Running it
 
- `wolf_sheep_model.py` runs the simulation and shows the population graph at the end.
- `app.py` runs the animated Solara visualization with sliders for population and reproduction thresholds.
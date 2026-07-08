from mesa.visualization import SolaraViz, make_space_component, make_plot_component
from wolf_sheep_model import WolfSheep, Sheep, Wolf, Grass
 
 
def agent_portrayal(agent):
    if isinstance(agent, Wolf):
        return {"color": "tab:red", "marker": "^", "size": 40, "zorder": 3}
    elif isinstance(agent, Sheep):
        return {"color": "tab:blue", "marker": "o", "size": 25, "zorder": 2}
    elif isinstance(agent, Grass):
        return {"color": "tab:green", "marker": "s", "size": 15, "zorder": 1}
    return {"color": "gray", "size": 10}
 
 
model_params = {
    "initial_sheep_population": {
        "type": "SliderInt",
        "value": 80,
        "label": "Initial Sheep Population",
        "min": 0,
        "max": 300,
        "step": 1,
    },
    "initial_wolf_population": {
        "type": "SliderInt",
        "value": 20,
        "label": "Initial Wolf Population",
        "min": 0,
        "max": 300,
        "step": 1,
    },
    "birth_rate_sheep": {
        "type": "SliderInt",
        "value": 7,
        "label": "Sheep Reproduction Threshold",
        "min": 0,
        "max": 9,
        "step": 1,
    },
    "birth_rate_wolf": {
        "type": "SliderInt",
        "value": 7,
        "label": "Wolf Reproduction Threshold",
        "min": 0,
        "max": 9,
        "step": 1,
    },
    "w": 30,
    "h": 30,
}
 
model = WolfSheep()
 
SpaceComponent = make_space_component(agent_portrayal)
PlotComponent = make_plot_component(
    {"sheep_count": "tab:blue", "wolf_count": "tab:red", "grass_count": "tab:green"}
)
 
page = SolaraViz(
    model,
    components=[SpaceComponent, PlotComponent],
    model_params=model_params,
    name="Wolf-Sheep-Grass Predator-Prey Model",
    play_interval = 10
)

import random
from mesa import Agent
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt

random.seed(312)

class Sheep(Agent):
    def __init__(
        self, 
        model, 
        initial_energy=20, 
        initial_age=0
    ):
        super().__init__(model)
        self.energy = initial_energy
        self.age = initial_age
        
    
    def move(self):
        if(self.energy>0):
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True)
            new_position = random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

    def reproduce(self):
        reproduction_chance = random.randint(0,9)
        reproduction_cost = 7
        if self.energy+3 > reproduction_cost and reproduction_chance>self.model.reproduction_rate_sheep: 
            new_child = self.__class__(self.model, initial_energy=reproduction_cost+5)
            self.model.grid.place_agent(new_child, self.pos)
            self.energy -= reproduction_cost
    
    def eat(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        grass = [obj for obj in cell_contents if isinstance(obj, Grass)]
        if self.energy<20 and grass:
            self.energy += 1
            self.model.grid.remove_agent(grass[0])
            grass[0].remove()
    
    def die(self):
        if self.energy<=0 or self.age>1000000000:
            self.model.grid.remove_agent(self)
            self.remove()

    def step(self):
        self.age+=1
        self.energy -= 1
        self.move()
        self.eat()
        self.reproduce()
        self.die()


# class Wolf(Sheep):
#     ##later override the move to add if no food move another step

#     def reproduce(self):
#         reproduction_chance = random.randint(0,9)
#         if self.energy>7 and reproduction_chance>self.model.reproduction_rate_wolf: ##defined in the model 
#             new_child = self.__class__(self.model)
#             self.model.MultiGrid.place_agent(new_child, self.pos)
#             self.energy = self.energy/2
    
#     def eat(self):
#         cell_contents = self.model.MultiGrid.get_cell_list_contents([self.pos])
#         _sheep = [obj for obj in cell_contents if type(obj) is Sheep]
#         if self.energy<20 and _sheep:
#             self.energy += 1
#             self.model.MultiGrid.remove_agent(_sheep[0])
#             _sheep[0].remove()

class Grass(Agent):
    def __init__(self, model, initial_age=0):
        super().__init__(model)
        self.age = initial_age

    def spawn(self):
        if random.random()<0.3:
            possible_spawn = self.model.grid.get_neighborhood(self.pos, moore=True)
            new_position = random.choice(possible_spawn)
            cell_contents = self.model.grid.get_cell_list_contents([new_position])
            already_has_grass = any(isinstance(a, Grass) for a in cell_contents)
            if not already_has_grass:
                new_grass = Grass(self.model)
                self.model.grid.place_agent(new_grass, new_position)
            
    def die(self):
        if self.age>100000000:
            self.model.grid.remove_agent(self)
            self.remove()

    def step(self):
        self.age+=1
        self.spawn()
        self.die()

class Wolf(Agent):
    def __init__(
        self, 
        model, 
        initial_energy=20, 
        initial_age=0
    ):
        super().__init__(model)
        self.energy = initial_energy
        self.age = initial_age
        
    
    def move(self):
        if(self.energy>0):
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True)
            new_position = random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

    def reproduce(self):
        reproduction_chance = random.randint(0,9)
        reproduction_cost = 7
        if self.energy+3>reproduction_cost and reproduction_chance>self.model.reproduction_rate_wolf:  
            new_child = self.__class__(self.model, initial_energy=reproduction_cost+5)
            self.model.grid.place_agent(new_child, self.pos)
            self.energy -= reproduction_cost
    
    def eat(self):
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        _sheep = [obj for obj in cell_contents if isinstance(obj, Sheep)]
        if self.energy<20 and _sheep:
            self.energy += 2.5
            self.model.grid.remove_agent(_sheep[0])
            _sheep[0].remove()
    
    def die(self):
        if self.energy<=0 or self.age>1000000000:
            self.model.grid.remove_agent(self)
            self.remove()

    def step(self):
        self.age+=1
        self.energy -= 1
        self.move()
        self.eat()
        self.reproduce()
        self.die()

class WolfSheep(Model):
    
    def __init__(
        self,
        initial_sheep_population = 100,
        initial_wolf_population = 20,
        w = 30,
        h = 30,
        birth_rate_sheep = 5,
        birth_rate_wolf = 6
    ):
        super().__init__()
        self.grid = MultiGrid(width=w, height=h, torus=True)
        self.reproduction_rate_sheep = birth_rate_sheep
        self.reproduction_rate_wolf = birth_rate_wolf

        for s in range(initial_sheep_population):
            x = random.randrange(h)
            y = random.randrange(w)
            sheep_pos = (x,y)
            new_sheep = Sheep(self)
            self.grid.place_agent(new_sheep, sheep_pos)

        for o in range(initial_wolf_population):
                p = random.randrange(h)
                q = random.randrange(w)
                wolf_pos = (p,q)
                new_wolf = Wolf(self)
                self.grid.place_agent(new_wolf, wolf_pos)
    
        for i in range(h):
            for j in range(w):
                if random.random()<0.6:
                    new_grass = Grass(self)
                    self.grid.place_agent(new_grass, (i,j))
                    
        
        self.datacollector = DataCollector(
            model_reporters={
                "sheep_count": "count_sheep",
                "wolf_count" : "count_wolf",
                "grass_count": "count_grass"
            }
        )

    
    @property
    def count_sheep(self):
        return len([a for a in self.agents if type(a) is Sheep])
    @property
    def count_wolf(self):
        return len([a for a in self.agents if type(a) is Wolf])
    @property
    def count_grass(self):
        return len([a for a in self.agents if type(a) is Grass])

    
    def step(self):
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")


model = WolfSheep()
for i in range(2000):
    model.step()
    if (i+1)%100 == 0:
        print(f"step {i} done..")

df = model.datacollector.get_model_vars_dataframe()
print(df.head(5))
print(df.tail(5))

df.plot()
plt.show()
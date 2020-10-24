from classes.universe import Universe
import pickle
from classes.universe import Swarm

"""
# This is if you want to test a swarm you have saved

with open("Best_Swarm_0.0001406299.txt", "rb") as fp:
    DNA = pickle.load(fp)

swarm = Swarm(DNA)

print(swarm.evaluate_swarm(True))
"""

universe = Universe(8) #8 swarms per generation

universe.Let_there_be_light(1) #100 generations


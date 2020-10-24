from classes.fireflie import Fireflie

import numpy as np
import pickle 
import matplotlib.pyplot as plt


class Swarm:
    def __init__(self, DNA):
        self.DNA = DNA
        
        self.time_phrame = 0.01  
        self.nb_of_fireflies = 40                          #Needs to be even. for the 3rd neighbor selection
        self.nb_of_neighbors = 8
        self.nb_of_iterations = 500 
        self.frequency = 1    # frequency of the blink
        self.swarm = []

        self.Data = [] # cointains arrays of the serial nbs that blinked. index = iteration

        for i in range(self.nb_of_iterations):
            self.Data.append([])

        #Initialize all the fireflies
        for i in range(self.nb_of_fireflies):
            self.swarm.append(Fireflie(self, i, self.DNA))

    def fitness_func(self):
        """
        This function measures the degree to which the swarm is in sync by doing
        the mean of every combination of distances(of their self.clock) between the fireflies
        """
        clocks = []
        dist_from_each_other = []
        for i in range(len(self.swarm)):
            clock = self.swarm[i].clock 
            clocks.append(clock)
        """
        for i in range(len(self.swarm)):
            for j in range(len(self.swarm)):
                if i != j:
                    dist = abs(clocks[i]-clocks[j])
                    if dist >= 0.5:
                        dist = 1 - dist
                    dist_from_each_other.append(dist)

        if np.var(dist_from_each_other) > 0.04:
            pass #print(dist_from_blink)
        
        return abs(np.mean(dist_from_each_other))
        """
        dist_from_blink = []
        for i in range(len(self.swarm)):
            clock = self.swarm[i].clock 
            if clock <= self.frequency/2:
                dist_from_blink.append(clock)
            else:
                dist_from_blink.append(self.frequency - clock)

        if np.var(dist_from_blink) > 0.04:
            pass #print(dist_from_blink)
        
        return np.var(dist_from_blink)


    def draw(self, iteration):
        """
        This is a cycle of the simulation the swarm
        """
        for i in range(len(self.swarm)):
            self.swarm[i].update_clock()
            self.swarm[i].check_blink(iteration)

    def evaluate_swarm(self, Show_graphs):
        """
        Main function to evaluate the fitness of the swarm's DNA
        """
        aggregated_fitness = 0
        start_aggregation = round(self.nb_of_iterations*0.9)

        if Show_graphs:
            data_x = []
            data_y = []

        #Do the simulation
        for i in range(self.nb_of_iterations):
            self.draw(i)
            if Show_graphs and i % 11 == 0:
                data_x.append(i)
                fitness = self.fitness_func()
                if fitness > 0.04:
                    fitness = 0.04
                data_y.append(fitness)
                print(str(round(i/self.nb_of_iterations*100)) + "%")

            if i >= start_aggregation:
                fitness = self.fitness_func()
                aggregated_fitness += fitness
        
        aggregated_fitness = aggregated_fitness / (self.nb_of_iterations-start_aggregation)
        
        #Show the results
        if Show_graphs:
            plt.plot(data_x, data_y)
            plt.show()
            with open("Data_simulation_" + str(aggregated_fitness) + ".txt", "wb") as fp:
                pickle.dump(self.Data, fp)

            for i in range(100):
                print(self.Data[len(self.Data) - i-1])

        """
        #Check for resonance hack
        Last_blinks = self.Data[len(self.Data) - 100:] #2d array containing the activity during the last 100 iterations
        seen = []
        seen_twice = []
        for i in Last_blinks:
            for j in i:
                if j in seen:
                    if j in seen_twice:
                        return 5
                    else:
                        seen_twice.append(j)
                else:
                    seen.append(j)
        """
        
        return aggregated_fitness




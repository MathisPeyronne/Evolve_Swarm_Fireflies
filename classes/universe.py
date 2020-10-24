import random
import pickle
import math
import struct
import sys

from classes.swarm import Swarm


class Universe:

    def __init__(self, nb_of_swarms = 8):
        self.nb_of_swarms = nb_of_swarms
        self.best_swarm = [20,[]]  #[fitness, DNA]
        self.current_population = []
        for i in range(nb_of_swarms):
            #randomly initialise everyone's DNA
            DNA = []
            for i in range(321):
                DNA.append(random.uniform(-1,1))
            
            self.current_population.append(DNA)

    def evaluate_swarms(self):
        """
        Compute the fitness of each swarm(by running each in a simulation)
        Output: the fitness distribution 
        """

        fitness_distribution = []

        for i in range(len(self.current_population)):

            swarm = Swarm(self.current_population[i])
            fitness = swarm.evaluate_swarm(False)
            if fitness < self.best_swarm[0]:
                self.best_swarm[0] = fitness 
                self.best_swarm[1] = self.current_population[i]
            
            
            
            print("fitness swarm #" + str(i) + ": " + str(fitness)) 
            fitness_distribution.append(fitness)

        return fitness_distribution

    def compute_prob_distribution(self, fitness_distribution):
        """
        fitness distribution --> probability distribution
        """

        fitness_distribution = [x**-2 for x in fitness_distribution]
        prob_distribution = []
        total = sum(fitness_distribution)

        for fitness in fitness_distribution:
            prob_distribution.append(fitness/total)

        return prob_distribution


    def produce_next_generation(self, prob_distribution, current_population):
        """
		* Pick two parents(according to fitness distribution)
		* Crossover - create a "child" by combining the DNA of the two parents
        * Mutation - mutate the child's DNA based on a given prob(mutation rate)
        """

        indexed_list = list(enumerate(current_population))
        parents_tuples = random.choices(indexed_list, prob_distribution, k=self.nb_of_swarms*2)
        
        parents_tuples = [(parents_tuples[i], parents_tuples[i+1]) for i in range(0, len(parents_tuples), 2)]
        
        next_population = []

        for DNA_p1, DNA_p2 in parents_tuples:
            mutation_rate = (1-prob_distribution[DNA_p1[0]])/30 #100    #the more the fitness of the parent, the less the mutation rate.
            next_population.append(self.make_a_child(DNA_p1[1], DNA_p2[1], mutation_rate))
    
        return next_population

    def bin64_to_float(self, b):
        """ Convert binary string to a float. """
        bf = (int(b, 2)).to_bytes(8, byteorder="big")
        return struct.unpack('>d', bf)[0]

    def float_to_bin64(self, value): 
        """ Convert float to 64-bit binary string. """
        [d] = struct.unpack(">Q", struct.pack(">d", value))
        return '{:064b}'.format(d)

    def make_a_child(self, DNA_p1, DNA_p2, mutation_rate):
        """
        * Crossover - create a "child" by combining the DNA of the two parents.          
        * Mutation - mutate the child's DNA based on a given prob(mutation rate)
        """

        #transform in bits
        DNA_p1_bit = "" 
        DNA_p2_bit = "" 

        for node in DNA_p1:
            DNA_p1_bit += self.float_to_bin64(node)
        
        for node in DNA_p2:
            DNA_p2_bit += self.float_to_bin64(node)

        #crossover

        DNA_child_bit = ""
        DNA_child = []
        nb_of_slices = int(len(DNA_p1)/4)  #It means that one slice will take up on average 4 coefficients(bytes)
        DNA_lenght = len(DNA_p1_bit)
        Slicing_indexes = [math.floor(random.random()*DNA_lenght) for i in range(nb_of_slices)]
        Slicing_indexes.append(0)
        Slicing_indexes.append(len(DNA_p1_bit))
        Slicing_indexes.sort()

        for i in range(1, len(Slicing_indexes)):
            if i%2 == 0:
                DNA_child_bit += DNA_p1_bit[Slicing_indexes[i-1]: Slicing_indexes[i]]
            else:
                DNA_child_bit += DNA_p2_bit[Slicing_indexes[i-1]: Slicing_indexes[i]]

        #Convert back to string
        length_of_bit = len(self.float_to_bin64(int(DNA_p1[0])))
        for i in range(len(DNA_p1)):
            DNA_child.append(self.bin64_to_float(DNA_child_bit[(i)*(length_of_bit):(i+1)*(length_of_bit)]))

        #do the mutation
        for i in range(len(DNA_child)):
            if random.random() > (1-mutation_rate):
                DNA_child[i] = random.uniform(-1,1)

        return DNA_child

    def Let_there_be_light(self, nb_of_generations):
        """
        * Put everything together
            * compute fitness of current population => fitness distribution
            * create next generation using this fitness distribution and old population
            * Repeat 
        """
        for i in range(nb_of_generations):
            print("Generation #" + str(i))
            fitness_distribution = self.evaluate_swarms()
            prob_distribution = self.compute_prob_distribution(fitness_distribution)
            #print(prob_distribution)
            self.next_generation = self.produce_next_generation(prob_distribution, self.current_population)

            self.current_population = self.next_generation
            self.current_population.append(self.best_swarm[1])
            print("Best swarm fitness: " + str(self.best_swarm[0]) )

        swarm = Swarm(self.best_swarm[1])
        fitness = swarm.evaluate_swarm(True)

        #store the best swarm
        with open("Best_Swarm_" + ('%.10f' % fitness) + ".txt", "wb") as fp:
            pickle.dump(self.best_swarm[1], fp)



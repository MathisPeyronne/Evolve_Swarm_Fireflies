import random
import numpy as np


class Fireflie:
    def __init__(self, swarm_object, _serial_nb, DNA):  

        self.time_phrame = swarm_object.time_phrame  
        self.frequency = swarm_object.frequency

        self.swarm_object = swarm_object

        self.swarm = swarm_object.swarm
        
        self.delay = round(random.random(), 4)  #btw 0 and 1

        self.nb_of_fireflies = swarm_object.nb_of_fireflies
        
        self.serial_nb = _serial_nb

        self.nb_of_neighbors = swarm_object.nb_of_neighbors

        self.neighbors = []
        #direct neighbors
        self.neighbors.append((self.serial_nb-1) % self.nb_of_fireflies)
        self.neighbors.append((self.serial_nb+1) % self.nb_of_fireflies)

        for i in range(self.nb_of_neighbors-2):
            self.neighbors.append((self.serial_nb + (i+1)*round(self.nb_of_fireflies/(self.nb_of_neighbors-1))) % self.nb_of_fireflies)


        self.clock = self.delay * self.frequency  

        #store the weights given by the DNA in variables
        self.W1 = DNA[:16] # 0 --> 15
        self.b1 = DNA[16:32] #16 --> 31
        self.W2 = DNA[32:(16*16)+32] #32 --> 287
        self.b2 = DNA[(16*16)+32:(16*16)+32+16] #288 --> 303
        self.W3 = DNA[-17:-1] # 304 --> 319
        self.b3 = DNA[-1] # 320 

        self.W1 = np.reshape(self.W1, (16,1))  #16 times 1 weight 
        self.b1 = np.reshape(self.b1, (16,1))

        self.W2 = np.reshape(self.W2, (16,16))
        self.b2 = np.reshape(self.b2, (16,1))  

        self.W3 = np.reshape(self.W3, (1,16))
        self.b3 = np.reshape(self.b3, (1,1))   

        """  
        print("delay: " + str(self.delay))
        print("serial_nb: " + str(self.serial_nb))
        print("neighbor1: " + str(self.neighbors[0]))
        print("neighbor2: " + str(self.neighbors[1]))
        print("clock: " + str(self.clock))
        """

    def forward_propagation(self):
        """
        The neural network will take the self.clock and choose a corresponding nudge
        """

        Z1 = np.dot(self.W1, np.reshape(self.clock, (1,1))) + self.b1
        A1 = self.Relu(Z1)
        Z2 = np.dot(self.W2, A1) + self.b2
        A2 = self.Relu(Z2)
        Z3 = np.dot(self.W3, A2) + self.b3
        A3 = self.sigmoid(Z3)

        return A3

    def update_clock(self):
        self.clock += self.time_phrame

    def check_blink(self, iteration):
        """
        Signal neighbors that he blinked if it is the case
        """
        if self.clock >= self.frequency:
            self.clock = self.clock % self.frequency
            self.swarm_object.Data[iteration].append(self.serial_nb)
            for i in range(self.nb_of_neighbors):
                self.swarm[self.neighbors[i]].neighbor_blinked()

    def neighbor_blinked(self):
        """
        neighbor blinked => compute and apply nudge
        """
        nudge = self.forward_propagation()

        self.clock += nudge

    def sigmoid(self, z):
        s = 1/(1+np.exp(-z))
        return s

    def Relu(self, z):
        s = np.maximum(z,0)
        return s
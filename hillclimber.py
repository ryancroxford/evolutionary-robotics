import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
from solution import Solution
import copy


class HillClimber:
    def __init__(self):
        self.parent = Solution()
        self.child = None

    def Evolve(self):
        self.parent.Evaluate("GUI")
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        print('\n', self.parent.fitness, self.child.fitness)
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child

    def Show_Best(self):
        self.parent.Evaluate("GUI")
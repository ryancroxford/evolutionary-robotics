import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
from solution import Solution
import copy


class ParallelHillClimber:
    def __init__(self):
        self.parents = dict()
        self.children = dict()
        self.nextAvailableID = 0
        self.child = None
        for i in range(c.populationSize):
            self.parents[i] = Solution(self.nextAvailableID)
            self.nextAvailableID += 1
        # self.child = None

    def Evaluate(self, solutions):
        for key in solutions:
            solutions[key].Start_Simulation("DIRECT")
        for key in solutions:
            solutions[key].Wait_For_Simulation_To_End()

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        # exit()
        self.Print()
        # print('\n', self.parent.fitness, self.child.fitness)
        self.Select()

    def Spawn(self):
        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for key in self.children:
            self.children[key].Mutate()

    def Select(self):
        for key in self.parents:
            if self.parents[key].fitness > self.children[key].fitness:
                self.parents[key] = self.children[key]

    def Show_Best(self):
        bestParent = None
        bestFitness = 100000
        for key in self.parents:
            parent = self.parents[key]
            if parent.fitness < bestFitness:
                bestParent = parent
                bestFitness = parent.fitness
        print(bestFitness)
        bestParent.Start_Simulation("GUI")
        pass

    def Print(self):
        print()
        for key in self.parents:
            print(f"Parent's fitness: {self.parents[key].fitness}, child fitness {self.children[key].fitness}")
        print()

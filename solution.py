import random

import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
import numpy as np
import os


class Solution:
    def __init__(self):
        self.weights = np.random.rand(3, 2)
        self.weights = self.weights * 2 - 1
        self.fitness = None

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py {directOrGUI}")
        inFileName = "fitness.txt"
        try:
            inFile = open(inFileName, 'r')
            self.fitness = float(inFile.read())
            inFile.close()
        except IOError:
            print(f"Error opening {inFileName}")

    def Mutate(self):
        randRow = random.randint(0, 2)
        randCol = random.randint(0, 1)
        self.weights[randRow, randCol] = random.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        length = 1
        width = 1
        height = 1
        x = 2
        y = 2
        z = height / 2
        pyrosim.Send_Cube(name="Box", pos=[x + 2, y + 2, z],
                          size=[length, width, height])

        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        length = 1
        width = 1
        height = 1
        x = 1.5
        y = 0
        z = 1.5
        pyrosim.Send_Cube(name="Torso", pos=[x, y, z], size=[length, width, height])
        # Create back leg
        pyrosim.Send_Joint(name="Torso_Back_Leg", parent="Torso", child="Back_Leg",
                           type="revolute", position="1.0 0.0 1.0")
        x = -0.5
        z = -0.5
        pyrosim.Send_Cube(name="Back_Leg", pos=[x, y, z],
                          size=[length, width, height])
        # Create front leg
        pyrosim.Send_Joint(name="Torso_Front_Leg", parent="Torso",
                           child="Front_Leg", type="revolute",
                           position="2.0 0.0 1.0")
        x = 0.5
        z = -0.5
        pyrosim.Send_Cube(name="Front_Leg", pos=[x, y, z],
                          size=[length, width, height])
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        sensor_names = ["Torso", "Back_Leg", "Front_Leg"]
        motor_names = ["Torso_Back_Leg", "Torso_Front_Leg"]

        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="Back_Leg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="Front_Leg")
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_Back_Leg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_Front_Leg")
        for currentRow in range(len(sensor_names)):
            for currentCol in range(len(motor_names)):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentCol + len(sensor_names),
                                     weight=self.weights[currentRow][currentCol])

        pyrosim.End()


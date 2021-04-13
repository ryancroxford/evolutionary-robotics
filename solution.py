import random

import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
import numpy as np
import os
import time

class Solution:
    def __init__(self, nextAvailableID):
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1
        self.fitness = None
        self.myID = nextAvailableID

    def Set_ID(self, ID):
        self.myID = ID

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        inFileName = f"fitness{self.myID}.txt"
        while not os.path.exists(inFileName):
            time.sleep(0.01)
        try:
            # print(f'opening: {inFileName}')
            inFile = open(inFileName, 'r')
            line = inFile.read()
            self.fitness = float(line)
            # print(self.fitness)
            inFile.close()
            os.system(f"rm fitness{self.myID}.txt")
        except IOError:
            print(f"Error opening {inFileName}")

    def Mutate(self):
        randRow = random.randint(0, c.numSensorNeurons - 1)
        randCol = random.randint(0, c.numMotorNeurons - 1)
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
        # cubes = [["Torso", [0.0, 0.0, 1.0], [1.0, 1.0, 1.0]],
        #          ["Back_Leg", [0.0, -0.5, 0.0], [0.2, 1, 0.2]],
        #          ["Front_Leg", [0.0, 0.5, 0.0], [0.2, 1, 0.2]],
        #          ["Left_Leg", [0,0,1], [1,1,1]],
        #          ["Torso", [0,0,1], [1,1,1]],
        #          ["Torso", [0,0,1], [1,1,1]],
        #          ["Torso", [0,0,1], [1,1,1]],
        #          ["Torso", [0,0,1], [1,1,1]],
        #          ["Torso", [0,0,1], [1,1,1]]]


        length = 1
        width = 1
        height = 1
        x = 0
        y = 0
        z = 1
        pyrosim.Send_Cube(name="Torso", pos=[x, y, z], size=[length, width, height])
        # Create back leg
        pyrosim.Send_Joint(name="Torso_Back_Leg", parent="Torso", child="Back_Leg",
                           type="revolute", position="0.0 -0.5 1.0", jointAxis="1 0 0")
        x = 0.0
        y = -0.5
        z = 0.0
        length = 0.2
        width = 1.0
        height = 0.2
        pyrosim.Send_Cube(name="Back_Leg", pos=[x, y, z],
                          size=[length, width, height])
        # Create front leg
        pyrosim.Send_Joint(name="Torso_Front_Leg", parent="Torso",
                           child="Front_Leg", type="revolute",
                           position="0.0 0.5 1.0", jointAxis="1 0 0")
        x = 0.0
        y = 0.5
        z = 0.0
        pyrosim.Send_Cube(name="Front_Leg", pos=[x, y, z],
                          size=[length, width, height])

        # Create left leg
        pyrosim.Send_Joint(name="Torso_Left_Leg", parent="Torso",
                           child="Left_Leg", type="revolute",
                           position="-0.5 0.0 1.0", jointAxis="1 0 0")
        x = -0.5
        y = 0.0
        z = 0.0
        length = 1.0
        width = 0.2
        height = 0.2
        pyrosim.Send_Cube(name="Left_Leg", pos=[x, y, z],
                          size=[length, width, height])

        # Create right leg
        pyrosim.Send_Joint(name="Torso_Right_Leg", parent="Torso",
                           child="Right_Leg", type="revolute",
                           position="0.5 0.0 1.0", jointAxis="1 0 0")
        x = 0.5
        y = 0.0
        z = 0.0
        pyrosim.Send_Cube(name="Right_Leg", pos=[x, y, z],
                          size=[length, width, height])

        # Create front lower leg
        pyrosim.Send_Joint(name="Front_Lower_Leg_Joint", parent="Front_Leg",
                           child="Front_Lower_Leg", type="revolute",
                           position="0.0 1.0 0.0", jointAxis="1 0 0")
        x = 0.0
        y = 0.0
        z = -0.5
        length = 0.2
        width = 0.2
        height = 1.0
        pyrosim.Send_Cube(name="Front_Lower_Leg", pos=[x, y, z],
                          size=[length, width, height])

        # Create back lower leg
        pyrosim.Send_Joint(name="Back_Lower_Leg_Joint", parent="Back_Leg",
                           child="Back_Lower_Leg", type="revolute",
                           position="0.0 -1.0 0.0", jointAxis="1 0 0")
        x = 0.0
        y = 0.0
        z = -0.5
        length = 0.2
        width = 0.2
        height = 1.0
        pyrosim.Send_Cube(name="Back_Lower_Leg", pos=[x, y, z],
                          size=[length, width, height])

        # Create left lower leg
        pyrosim.Send_Joint(name="Left_Lower_Leg_Joint", parent="Left_Leg",
                           child="Left_Lower_Leg", type="revolute",
                           position="-1.0 0.0 0.0", jointAxis="1 0 0")
        x = 0.0
        y = 0.0
        z = -0.5
        length = 0.2
        width = 0.2
        height = 1.0
        pyrosim.Send_Cube(name="Left_Lower_Leg", pos=[x, y, z],
                          size=[length, width, height])

        # Create right lower leg
        pyrosim.Send_Joint(name="Right_Lower_Leg_Joint", parent="Right_Leg",
                           child="Right_Lower_Leg", type="revolute",
                           position="1.0 0.0 0.0", jointAxis="1 0 0")
        x = 0.0
        y = 0.0
        z = -0.5
        length = 0.2
        width = 0.2
        height = 1.0
        pyrosim.Send_Cube(name="Right_Lower_Leg", pos=[x, y, z],
                          size=[length, width, height])

        pyrosim.End()


    def Create_Joint(self, name, parent, child, type, position, jointAxis):
        pyrosim.Send_Joint(name=name, parent=parent,
                           child=child, type=type,
                           position=position, jointAxis=jointAxis)

    def Create_Cube(self, name, position, size):
        pyrosim.Send_Cube(name=name, pos=position,
                          size=size)

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        sensor_names = ["Back_Lower_Leg", "Front_Lower_Leg", "Left_Lower_Leg", "Right_Lower_Leg"]
        motor_names = ["Torso_Back_Leg", "Torso_Front_Leg", "Torso_Left_Leg", "Torso_Right_Leg",
                       "Front_Lower_Leg_Joint", "Back_Lower_Leg_Joint", "Left_Lower_Leg_Joint", "Right_Lower_Leg_Joint"]

        i = 0
        for sensor_name in sensor_names:
            pyrosim.Send_Sensor_Neuron(name=i, linkName=sensor_name)
            i += 1

        j = 0
        for motor_name in motor_names:
            pyrosim.Send_Motor_Neuron(name=j+i, jointName=motor_name)
            j += 1

        for currentRow in range(c.numSensorNeurons):
            for currentCol in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentCol + c.numSensorNeurons,
                                     weight=self.weights[currentRow][currentCol])

        pyrosim.End()

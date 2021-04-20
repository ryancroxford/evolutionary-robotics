from motor import Motor
from sensor import Sensor
import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os


class Robot:
    def __init__(self, solutionID):
        self.sensors = dict()
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate("body.urdf")
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.solutionID = solutionID
        os.system(f"rm brain{self.solutionID}.nndf")

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = Sensor(linkName)

    def Sense(self, t):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = dict()
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = Motor(jointName)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(desiredAngle, self.robot)

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robot)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        zPosition = basePosition[2]
        outFileName = f"tmp{self.solutionID}.txt"
        try:
            outFile = open(outFileName, 'w')
            outFile.write(str(zPosition))
            outFile.close()
            # print(f"Writing {outFileName}")
            os.system(f"mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt")
        except IOError:
            print(f"Error opening {outFileName}")

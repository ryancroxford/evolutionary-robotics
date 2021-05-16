from motor import Motor
from sensor import Sensor
import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import numpy as np


class Robot:
    def __init__(self, solutionID):
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate("body.urdf")
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.solutionID = solutionID
        os.system(f"rm brain{self.solutionID}.nndf")

    def Prepare_To_Sense(self):
        self.sensors = dict()
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
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(desiredAngle, self.robot)

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        lowerLinkNames = ["Back_Leg", "Front_Leg"]
        lowerLinkSensorValues_array = []
        for linkName in lowerLinkNames:
            print(linkName)
            lowerLinkSensorValues_array.append(self.sensors[linkName].values)
        lowerLinkSensorValues_tuple = tuple(lowerLinkSensorValues_array)
        lowerLinkSensorValues = np.vstack(lowerLinkSensorValues_array)
        print(lowerLinkSensorValues)
        lowerLinkSensorValues_means = np.mean(lowerLinkSensorValues, axis=0)
        print(lowerLinkSensorValues_means)
        try:
            idx_pairs = np.where(np.diff(np.hstack(([False],
                                                    lowerLinkSensorValues_means == -1,
                                                    [False]))))[0].reshape(-1, 2)
            print(idx_pairs)
            longestFlightTime = idx_pairs[np.diff(idx_pairs, axis=1).argmax(), 1] - idx_pairs[
                np.diff(idx_pairs, axis=1).argmax(), 0]
        except ValueError:
            longestFlightTime = 0

        heights = [self.sensors["Torso"].values]
        maxHeight = np.amax(heights)
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robot)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        zPosition = basePosition[2]
        outFileName = f"tmp{self.solutionID}.txt"
        fitness = longestFlightTime * maxHeight * (-xPosition)
        try:
            outFile = open(outFileName, 'w')
            outFile.write(str(fitness))
            outFile.close()
            # print(f"Writing {outFileName}")
            os.system(f"mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt")
        except IOError:
            print(f"Error opening {outFileName}")

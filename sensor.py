import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim


class Sensor:
    def __init__(self, linkName):
        self.values = np.zeros(c.ITERATIONS)
        self.linkName = linkName

    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        if t == c.ITERATIONS - 1:
            self.Save_Values()

    def Save_Values(self):
        np.save(f"./data/{self.linkName}_touch.npy", self.values)

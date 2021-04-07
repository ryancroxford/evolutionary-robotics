import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p


class Motor:
    def __init__(self, jointName):
        self.values = np.zeros(c.ITERATIONS)
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.PI/3
        print(self.jointName)
        if self.jointName == "Torso_Back_Leg":
            self.frequency = c.frequencyBackLeg
            print(c.frequencyBackLeg)
        else:
            self.frequency = c.frequencyFrontLeg
            print(c.frequencyFrontLeg)
        self.offset = 0
        self.targetAngles = np.sin(self.frequency * np.linspace(-(c.PI), c.PI, c.ITERATIONS)
                                   + self.offset) * self.amplitude

    def Set_Value(self, t, robot):
        self.values[t] = pyrosim.Set_Motor_For_Joint(
                                 bodyIndex=robot,
                                 jointName=self.jointName,
                                 controlMode=p.POSITION_CONTROL,
                                 targetPosition=self.targetAngles[t],
                                 maxForce=c.maxForceFrontLeg)

    def Save_Values(self):
        np.save(f"./data/target_angles_{self.jointName}.npy", self.values)

import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p


class Motor:
    def __init__(self, jointName):
        self.values = np.zeros(c.ITERATIONS)
        self.jointName = jointName

    def Set_Value(self, desiredAngle, robot):
        pyrosim.Set_Motor_For_Joint(bodyIndex=robot,
                                    jointName=self.jointName,
                                    controlMode=p.POSITION_CONTROL,
                                    targetPosition=desiredAngle,
                                    maxForce=c.maxForceFrontLeg)

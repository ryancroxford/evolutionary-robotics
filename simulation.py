from world import World
from robot import Robot
import pybullet as p
import pybullet_data
import constants as c
import time


class Simulation:
    def __init__(self, directOrGUI):
        self.directOrGUI = directOrGUI
        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.ZERO, c.ZERO, c.GRAVITY)
        self.world = World()
        self.robot = Robot()

    def Run(self):
        for t in range(c.ITERATIONS):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            if self.directOrGUI != "DIRECT":
                time.sleep(c.TIME_STEP)

    def __del__(self):
        p.disconnect()

    def Get_Fitness(self):
        self.robot.Get_Fitness()

from world import World
from robot import Robot
import pybullet as p
import pybullet_data
import constants as c


class Simulation:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.ZERO, c.ZERO, c.GRAVITY)
        self.world = World()
        self.robot = Robot()

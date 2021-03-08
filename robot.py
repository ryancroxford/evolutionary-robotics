from motor import Motor
from sensor import Sensor
import pybullet as p
import pyrosim.pyrosim as pyrosim


class Robot:
    def __init__(self):
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate("body.urdf")
        self.sensors = dict()
        self.motors = dict()

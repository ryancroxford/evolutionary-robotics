import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np

ITERATIONS = 1000

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
bodyId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate("body.urdf")

backLegSensorValues = np.zeros(ITERATIONS)
frontLegSensorValues = np.zeros(ITERATIONS)


for i in range(ITERATIONS):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Back_Leg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Front_Leg")
    time.sleep(1/60)

np.save("./data/back_leg_touch.npy", backLegSensorValues)
np.save("./data/front_leg_touch.npy", frontLegSensorValues)

p.disconnect()

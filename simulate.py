import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c

# Set up the physicsClient load in the world and robot
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(c.ZERO, c.ZERO, c.GRAVITY)
planeId = p.loadURDF("plane.urdf")
robot = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate("body.urdf")

# Create arrays to store sensor values
backLegSensorValues = np.zeros(c.ITERATIONS)
frontLegSensorValues = np.zeros(c.ITERATIONS)

# create and save a vector of targetAngles in a sinusoidal shape
targetAnglesBackLeg = np.sin(c.frequencyBackLeg * np.linspace(-c.PI, c.PI, c.ITERATIONS),
                             + c.phaseOffsetBackLeg) * c.amplitudeBackLeg
targetAnglesFrontLeg = np.sin(c.frequencyFrontLeg * np.linspace(-c.PI, c.PI, c.ITERATIONS)
                              + c.phaseOffsetFrontLeg) * c.amplitudeFrontLeg
# np.save("./data/target_angles_Back_Leg.npy", targetAnglesBackLeg)
# np.save("./data/target_angles_Front_Leg.npy", targetAnglesFrontLeg)
# exit()
# The main part of the stepSimulation, step through ITERATIONS amount of times
for i in range(c.ITERATIONS):
    p.stepSimulation()
    # store current sensor values
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Back_Leg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Front_Leg")
    # Add motors
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robot,
        jointName="Torso_Back_Leg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=targetAnglesBackLeg[i],
        maxForce=c.maxForceBackLeg)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robot,
        jointName="Torso_Front_Leg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=targetAnglesFrontLeg[i],
        maxForce=c.maxForceFrontLeg)
    # slow down the simulation
    time.sleep(c.TIME_STEP)

np.save("./data/back_leg_touch.npy", backLegSensorValues)
np.save("./data/front_leg_touch.npy", frontLegSensorValues)


p.disconnect()

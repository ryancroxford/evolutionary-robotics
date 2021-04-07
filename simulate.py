import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np

# Set constants
ITERATIONS = 1000
PI = np.pi

# Set up the physicsClient load in the world and robot
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
robot = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate("body.urdf")

# Create arrays to store sensor values
backLegSensorValues = np.zeros(ITERATIONS)
frontLegSensorValues = np.zeros(ITERATIONS)

# Create variables to alter the targetAngles
amplitudeBackLeg = PI/3
frequencyBackLeg = 10
phaseOffsetBackLeg = 0

amplitudeFrontLeg = PI/3
frequencyFrontLeg = 20
phaseOffsetFrontLeg = PI/3

# create and save a vector of targetAngles in a sinusoidal shape
targetAnglesBackLeg = np.sin(frequencyBackLeg * np.linspace(-PI, PI, ITERATIONS)
                             + phaseOffsetBackLeg) * amplitudeBackLeg
targetAnglesFrontLeg = np.sin(frequencyFrontLeg * np.linspace(-PI, PI, ITERATIONS)
                              + phaseOffsetFrontLeg) * amplitudeFrontLeg
# np.save("./data/target_angles_Back_Leg.npy", targetAnglesBackLeg)
# np.save("./data/target_angles_Front_Leg.npy", targetAnglesFrontLeg)
# exit()
# The main part of the stepSimulation, step through ITERATIONS amount of times
for i in range(ITERATIONS):
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
        maxForce=25)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robot,
        jointName="Torso_Front_Leg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=targetAnglesFrontLeg[i],
        maxForce=25)
    # slow down the simulation
    time.sleep(1/60)

np.save("./data/back_leg_touch.npy", backLegSensorValues)
np.save("./data/front_leg_touch.npy", frontLegSensorValues)


p.disconnect()

import numpy as np

ITERATIONS = 1500
PI = np.pi
GRAVITY = -9.8
MAX_FORCE = 25
TIME_STEP = (1/1020)
ZERO = 0


amplitudeBackLeg = PI/3
frequencyBackLeg = 10
phaseOffsetBackLeg = ZERO
maxForceBackLeg = 25

amplitudeFrontLeg = PI/3
frequencyFrontLeg = 20
phaseOffsetFrontLeg = PI/3
maxForceFrontLeg = 25

numberOfGenerations = 20
populationSize = 32

numSensorNeurons = 4
numMotorNeurons = 8
motorJointRange = 0.2

import numpy as np
import matplotlib.pyplot as plt

fitnessValues = np.load("./fitness.npy")

# for row in range(fitnessValues.shape[1]):
#      plt.plot(fitnessValues[row, :])

fitnessValuesMean = np.mean(fitnessValues, axis=0)
stdDev = np.std(fitnessValues, axis=0)
plt.plot(fitnessValuesMean-stdDev)
plt.plot(fitnessValuesMean, label="Mean", linewidth = 4)
plt.plot(fitnessValuesMean+stdDev)
# plt.plot(targetAnglesBackLeg, label="Back Leg Motor", linewidth = 4)
# plt.plot(targetAnglesFrontLeg, label="Front Leg Motor")
# plt.ylabel('sin(x)')
# plt.axis('tight')

plt.legend()

plt.show()

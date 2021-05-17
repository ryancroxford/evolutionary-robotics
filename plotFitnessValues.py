import numpy as np
import matplotlib.pyplot as plt

fitnessValuesA = np.load("./fitnessA.npy")
fitnessValuesB = np.load("./fitnessB.npy")

# for row in range(fitnessValues.shape[1]):
#      plt.plot(fitnessValues[row, :])

fitnessValuesMeanA = np.mean(fitnessValuesA, axis=0)
stdDevA = np.std(fitnessValuesA, axis=0)
plt.plot(fitnessValuesMeanA-stdDevA, label="Upper A")
plt.plot(fitnessValuesMeanA, label="Mean A", linewidth = 4)
plt.plot(fitnessValuesMeanA+stdDevA, label="Lower A")
fitnessValuesMeanB = np.mean(fitnessValuesB, axis=0)
stdDevB = np.std(fitnessValuesB, axis=0)
plt.plot(fitnessValuesMeanB-stdDevB, label="Upper B")
plt.plot(fitnessValuesMeanB, label="Mean B", linewidth = 4)
plt.plot(fitnessValuesMeanB+stdDevB, label="Lower B")

plt.legend()

plt.show()

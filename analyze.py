import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load("./data/back_leg_touch.npy")
frontLegSensorValues = np.load("./data/front_leg_touch.npy")

plt.plot(backLegSensorValues, label="Back Leg", linewidth=4)
plt.plot(frontLegSensorValues, label="Front Leg")
plt.legend()

plt.show()

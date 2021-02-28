import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load("./data/back_leg_touch.npy")
frontLegSensorValues = np.load("./data/front_leg_touch.npy")
targetAnglesBackLeg = np.load("./data/target_angles_Back_Leg.npy")
targetAnglesFrontLeg = np.load("./data/target_angles_Front_Leg.npy")

# plt.plot(backLegSensorValues, label="Back Leg", linewidth=4)
# plt.plot(frontLegSensorValues, label="Front Leg")


plt.plot(targetAnglesBackLeg, label="Back Leg Motor", linewidth = 4)
plt.plot(targetAnglesFrontLeg, label="Front Leg Motor")
plt.ylabel('sin(x)')
plt.axis('tight')

plt.legend()

plt.show()

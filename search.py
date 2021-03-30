import os
from hillclimber import HillClimber


# for i in range(5):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")

hc = HillClimber()
hc.Evolve()
hc.Show_Best()

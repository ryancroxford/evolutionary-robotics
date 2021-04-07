import os
from parallelHillClimber import ParallelHillClimber


# for i in range(5):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")

os.system("rm brain*.nndf")
os.system("rm fitness*.txt")
os.system("rm tmp*.txt")

phc = ParallelHillClimber()
phc.Evolve()
phc.Show_Best()

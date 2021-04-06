from simulation import Simulation
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]

simulation = Simulation(directOrGUI, solutionID)
simulation.Run()
simulation.Get_Fitness()


from simulation import Simulation
import sys

directOrGUI = sys.argv[1]

simulation = Simulation(directOrGUI)
simulation.Run()
simulation.Get_Fitness()


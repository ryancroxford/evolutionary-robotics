import pyrosim.pyrosim as pyrosim
import random


def Create_World():
    pyrosim.Start_SDF("world.sdf")
    length = 1
    width = 1
    height = 1
    x = 2
    y = 2
    z = height/2
    pyrosim.Send_Cube(name="Box", pos=[x+2, y+2, z],
                      size=[length, width, height])

    pyrosim.End()


def Create_Body():
    pyrosim.Start_URDF("body.urdf")
    length = 1
    width = 1
    height = 1
    x = 1.5
    y = 0
    z = 1.5
    pyrosim.Send_Cube(name="Torso", pos=[x, y, z], size=[length, width, height])
    # Create back leg
    pyrosim.Send_Joint(name="Torso_Back_Leg", parent="Torso", child="Back_Leg",
                       type="revolute", position="1.0 0.0 1.0")
    x = -0.5
    z = -0.5
    pyrosim.Send_Cube(name="Back_Leg", pos=[x, y, z],
                      size=[length, width, height])
    # Create front leg
    pyrosim.Send_Joint(name="Torso_Front_Leg", parent="Torso",
                       child="Front_Leg", type="revolute",
                       position="2.0 0.0 1.0")
    x = 0.5
    z = -0.5
    pyrosim.Send_Cube(name="Front_Leg", pos=[x, y, z],
                      size=[length, width, height])
    pyrosim.End()


def Create_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    sensor_names = ["Torso", "Back_Leg", "Front_Leg"]
    motor_names = ["Torso_Back_Leg", "Torso_Front_Leg"]

    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="Back_Leg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="Front_Leg")
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_Back_Leg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_Front_Leg")
    for i in range(len(sensor_names)):
        for j in range(len(sensor_names), len(motor_names) + len(sensor_names)):
            weight = random.uniform(-1,1)
            pyrosim.Send_Synapse(sourceNeuronName=i, targetNeuronName=j, weight=weight)

    pyrosim.End()


def main():
    Create_World()
    Create_Body()
    Create_Brain()


main()

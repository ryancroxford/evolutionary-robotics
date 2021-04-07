import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

# initalize size and positions
length = 1
width = 1
height = 1
x = 0
y = 0
z = height/2

# loop to create a 6x6 spread of 10 link tall towers
for i in range(6):
    for j in range(6):
        # reset size and initial z position
        length = 1
        width = 1
        height = 1
        z = height/2
        for k in range(10):
            x = i
            y = j
            pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
            # stack the next link on top of the previous
            z += height
            # make the next link's dimensions 90% as big
            height *= 0.9
            width *= 0.9
            length *= 0.9


pyrosim.End()

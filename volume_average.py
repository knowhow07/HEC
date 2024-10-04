#%%

# File paths
dump_file_path = '/Users/nuohaoliu/Library/CloudStorage/OneDrive-UW-Madison/laps_example/other/HEC/\
sqs/HfTiZrC/AIMD/NPT/'
input_file = 'XDATCAR'
output_file_path = 'volume'

# Import necessary libraries
import re
import numpy as np
import matplotlib.pyplot as plt

average_step = 200




# Read the heatup dump file to extract the last timestep
with open(dump_file_path+input_file, 'r') as f:
    dump_data = f.readlines()

with open(f"dump_data", "w") as f:
    f.write("\n".join(dump_data))
# print(dump_data)
# Initialize variables to track timesteps and positions
last_timestep_data = []
current_timestep_data = []
is_reading_atoms = False
current_timestep = None
last_timestep = None
# box_vector = np.empty((0,3)) 
# box_size = np.empty((0,3))
volumes = np.empty((0,2))




    

# Extract both the last timestep and the corresponding box size from the dump file

for step in range(0,int(len(dump_data)/72)):
    # is_reading_atoms = False  # Stop reading atom data temporarily
    # Read the next three lines for box size
    box_bounds = {}
    # bounds = dump_data[dump_data.index(line) + 2 + (64+8) * i].strip().split()
    # x=x
    for i, axis in enumerate(['x', 'y', 'z']):
        bounds = dump_data[2 + i + (64+8) * step ].strip().split()
        print(bounds)
        print( 2 + i + (64+8) * step)
        box_bounds[axis] = [float(bounds[0]), float(bounds[1]), float(bounds[2])]
    volume = np.linalg.norm(np.cross(box_bounds['x'], box_bounds['y']) * box_bounds['z'])
    volumes = np.append(volumes,np.reshape((step+1,volume),(1,2)),axis=0)
    # print(volume)
    # box_size = np.append(box_size, box_size_vector, axis=0)
            
# print(volumes)

volume_average = np.average(volumes[-average_step:,1])
print(volume_average)
box_vector = [volume_average ** (1/3), volume_average ** (1/3), volume_average ** (1/3)]
print(box_vector)

last_timestep = dump_data[-67:]


    
def convert_to_poscar(box_vectors, last_timestep,filename):
    # Extract unique elements and count them
    # Prepare POSCAR content
    poscar_lines = []

    # Title line
    poscar_lines.append("Generated POSCAR from average volume")

    # Scaling factor
    poscar_lines.append("1.0")

    # Lattice vectors from extracted box sizes
    poscar_lines.append(f"{box_vectors[0]} 0.0 0.0")
    poscar_lines.append(f"0.0 {box_vectors[1]} 0.0")
    poscar_lines.append(f"0.0 0.0 {box_vectors[2]}")
    # poscar_lines.append(f"average from last{average_step}".format())
    

    # poscar_lines.append(last_timestep)
    # Write to POSCAR file
    with open(f"{filename}", "w") as f:
        f.write("\n".join(poscar_lines))
        f.write("\n")
        for line in last_timestep:
            f.write(f"{line}")

    return f"{filename}"

convert_to_poscar(box_vector, last_timestep, dump_file_path + "POSCAR_ave")

# print(last_timestep_data)
#%%
plt.figure(figsize=(8, 6))
fig, ax = plt.subplots()
ax.plot(volumes[:,0], volumes[:,1], label='Volume')

# Calculate the box size vectors for the last timestep
# Add labels and title
plt.xlabel('Step')
plt.ylabel('Volume')
# plt.title('Step vs NPT Volume')

# # Show the plot with grid
# ax.grid(True)
# ax.legend()
plt.show()





# %%

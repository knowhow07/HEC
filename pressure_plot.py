#%%

# File paths
dump_file_path = '/Users/nuohaoliu/Library/CloudStorage/OneDrive-UW-Madison/laps_example/other/HEC/\
sqs/paper/VNbTaMoW/ave/4500K/'
input_file = 'XDATCAR'
output_file_path = 'volume'

# Import necessary libraries
import re
import numpy as np
import subprocess
from subprocess import call
import matplotlib.pyplot as plt
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

step_start = 200
step_end = 500
os.chdir(dump_file_path)
# subprocess.run(["cd" dump_file_path])
subprocess.run("pwd")
subprocess.run("grep 'external pressure' OUTCAR | awk '{print$4}' > pressure.txt",shell=True)
with open("pressure.txt", 'r') as f:
    pressure = f.read().splitlines()
    pressure = np.asarray(pressure, dtype = float)
    # energy = np.reshape(energy,(len(energy),1))
# rc = call(dir_path+"/energy.sh")
#
# print(type(energy))



# print(pressure[0:10])
# print(volumes[:,0].shape)
# print(last_timestep_data)
#%%

plt.figure(figsize=(9, 6))
font = {'size'   : 14}
plt.rc('font', **font)
fig, ax1 = plt.subplots()
color = 'tab:red'
# axs[0].plot(volumes[:,0], volumes[:,1], label='Volume')
# axs.stackplot(volumes[:,0], volumes[:,1],energy[:], labels=('Volume','Pressure'))
step = np.arange(1,len(pressure)+1)

from scipy.ndimage import uniform_filter1d
N = 20
pressure = uniform_filter1d(pressure, size=N)
ax1.plot(step, pressure, label='Pressure', color = color)
ax1.set_xlabel('Step')
ax1.set_ylabel('Pressure (Bar)', color=color)
ax1.tick_params(axis='y', labelcolor=color)
# # Show the plot with grid
plt.savefig('pressure.png',dpi=300)
plt.show()





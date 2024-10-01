# Local lattice distortion calculations for 64 atoms HECs
# File paths
input_file_path = '/Users/nuohaoliu/Library/CloudStorage/OneDrive-UW-Madison/\
laps_example/other/HEC/sqs/properties/distortion/VNbTaMoW/'
# hec_name = ""x
# crys_file = "file-name.vasp"
equi_file = "CONTCAR"
# output_file_path = 'POSCAR'
num_atoms = 64
bound = 0.15


# Import necessary libraries
import re
import pandas as pd
import numpy as np

# def detect_delimiter(filename, line_num):
#     # Common delimiters that might be used in text files
#     possible_delimiters = [',', '\t', ';', '|', ' ', ':']

#     with open(filename, 'r') as file:
#         line = file.readlines()[line_num]

#     # Try each delimiter and check if the split results in valid numbers
#     for delimiter in possible_delimiters:
#         split_numbers = line.split(delimiter)
        
#         # Check if all elements can be converted to float
#         try:
#             # If all parts are successfully converted to float, we've found the delimiter
#             if all(re.match(r"^-?\d+(?:\.\d+)?$", part) for part in split_numbers):
#                 return delimiter
#         except ValueError:
#             continue
#     # If no delimiter was found, return None
#     return None

# Read the heatup dump file to extract the last timestep
def element_coords(input_file_path, inputfile):
    with open(input_file_path + inputfile, 'r') as f:
        crys_data = []
        box_size = []
        crys_data = f.readlines()
        elements = crys_data[5].strip().split()
        elements_num = np.asarray(crys_data[6].strip().split(),dtype=int)
        box_size = np.append(box_size, crys_data[2].strip().split()[0])
        box_size = np.append(box_size, crys_data[3].strip().split()[1])
        box_size = np.append(box_size, crys_data[4].strip().split()[2])
        # print(box_size)
        # print(crys_data[2].strip().split()[0])
        # box_size[0] = np.asarray(crys_data[2].strip().split()[0],dtype=int)
        # box_size[1] = crys_data[3].strip().split()[1]
        # box_size[2] = crys_data[4].strip().split()[2]
    # print(elements_num)

    # Extract the 64 atoms coordinates to the coords_all
    for line_index, line in enumerate(crys_data):
        if "Direct" in line:
            coords_all = np.empty((0,3))
            
            for i in range(1,num_atoms+1):
                coord = np.reshape(crys_data[line_index + i].strip().split(),(1,3))
                coords_all = np.append(coords_all,coord,axis=0)
            # coords_all[coords_all>1] -= 1
            # print(coords_all.shape)
    # Save the coordinates to the coords seperately           
    coords = []
    start_idx = 0
    for n in elements_num:
        coords.append(coords_all[start_idx:start_idx + n, :])
        start_idx += n
    
    return coords, elements, box_size

def sqs_coords(input_file_path, inputfile):
    with open(input_file_path + inputfile, 'r') as f:
        crys_data = []
        crys_data = f.readlines()
        elements = crys_data[5].strip().split()
        elements_num = np.asarray(crys_data[6].strip().split(),dtype=int)
    # print(elements_num)

    # Extract the 64 atoms coordinates to the coords_all
    for line_index, line in enumerate(crys_data):
        if "Direct" in line:
            coords_all = np.empty((0,3))
            for i in range(1,num_atoms+1):
                coord = np.reshape(crys_data[line_index + i].strip().split(),(1,3))
                coords_all = np.append(coords_all,coord,axis=0)
            # coords_all[coords_all>1] -= 1
            # print(coords_all.shape)
    # Save the coordinates to the coords seperately    
    coords_all =  coords_all.astype(float) 
    # print(coords_all[0:5])
    coords_all[coords_all < bound] = 0
    # coords_all[coords_all < 0.26 | coords_all> 0.24] = 0.25
    coords_all = np.where((coords_all <= 0.25 + bound) & (coords_all >= 0.25 - bound), 0.25, coords_all )
    coords_all = np.where((coords_all <= 0.5 + bound) & (coords_all>= 0.5 - bound), 0.50, coords_all)
    coords_all = np.where((coords_all <= 0.75 + bound) & (coords_all >= 0.75 - bound),  0.75, coords_all)
    coords_all = np.where((coords_all <= 1.00 + bound) & (coords_all >= 1.00 - bound),  1.00, coords_all)
    # coords_all[(coords_all < 0.51) and (coords_all > 0.49)] = 0.50
    # coords_all[coords_all < 0.76 and coords_all > 0.74] = 0.75 
    # coords_all[coords_all < 0.99 and coords_all > 1.01] = 1.00
    # print(coords_all[0:5])
    coords = []
    start_idx = 0
    for n in elements_num:
        coords.append(coords_all[start_idx:start_idx + n, :])
        start_idx += n
    
    return coords, elements

def coordinate_difference(crys_coords, equi_coords, box_size):
    # Initialize a list to store the differences
    coord_diff = []
    
    # Iterate over each element's coordinates
    for crys_element_coords, equi_element_coords in zip(crys_coords, equi_coords):
        # Ensure that the shapes of the coordinates match
        crys_element_coords =  crys_element_coords.astype(float)
        equi_element_coords =  equi_element_coords.astype(float)
        # sqs results with use 1.0 instead of 0.0
        # crys_element_coords[crys_element_coords>=1.0] -= 1
        # crys_element_coords = np.absolute(crys_element_coords-1)
        # equi_element_coords = np.absolute(equi_element_coords-1)
        # print(crys_element_coords[0])
        # print(crys_element_coords[0])

        if crys_element_coords.shape == equi_element_coords.shape:
            # Subtract the corresponding coordinates
            diff = equi_element_coords.astype(float) - crys_element_coords.astype(float)
            diff =  diff.astype(float)
            diff = np.absolute(diff)
            diff[diff>0.5] -= 1
            # print(diff[0],"before")
            box_size = box_size.astype(np.float64)
            diff = diff * box_size
            # print(diff[0],"after")

            coord_diff.append(diff)

        else:
            raise ValueError(f"Shape mismatch between crys_coords and equi_coords for an element. "
                             f"Shapes are {crys_element_coords.shape} and {equi_element_coords.shape}.")

    return coord_diff


# crys_coords, elements1 = element_coords(input_file_path, crys_file)
crys_coords, _ = sqs_coords(input_file_path, equi_file)
print(crys_coords[0])
equi_coords, elements2, box_size = element_coords(input_file_path, equi_file)



coord_diff = coordinate_difference( crys_coords,equi_coords, box_size)


LLD = np.array([])
sum_all = 0
for idx, array in enumerate(coord_diff):
    
    sqrt_row = np.sqrt(np.sum(np.square(array), axis=1))
    # print(len(sqrt_row))
    sum_row = np.reshape(np.array(np.sum(sqrt_row, axis = 0)/len(sqrt_row)),(1,))
    sum_all += np.sum(sqrt_row, axis = 0) 
    # print(sum_row)
    # # sum_row = np.reshape(sum_row.shape,(1,))
    # print(LLD.shape)
    LLD = np.append(LLD, sum_row)
LLD_sum = sum_all  / num_atoms
# LLD_sum = np.sum(sum_row)

print(box_size)
for element, value in zip(elements2,LLD):
    print(element, value)
print("all", LLD_sum)

# check the shape of coords
# for idx, array in enumerate(coord_diff):
#     print(f"Array {idx + 1} shape: {array}")

# for idx, array in enumerate(equi_coords):
#     # print(f"Array {idx + 1} shape: {array.shape}")
#     diff = array 
#     print(diff.type)

                  
    








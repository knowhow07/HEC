

# File paths
dump_file_path = 'MD/heatup.lammpstrj'
output_file_path = 'POSCAR'
masses_file_path = 'MD/masses.txt'

# Import necessary libraries
import re
import pandas as pd


# Read the masses file to map element symbols to type IDs
with open(masses_file_path, 'r') as f:
    masses_data = f.readlines()
    


# Process the masses file to create a mapping dictionary
element_mapping = {}
for line in masses_data:
    match = re.match(r"mass(\d+)\s+([\d\.]+)\s+#\s+(\w+)", line.strip())
    if match:
        type_id = int(match.group(1))
        element = match.group(3)
        element_mapping[type_id] = element

# Read the heatup dump file to extract the last timestep
with open(dump_file_path, 'r') as f:
    dump_data = f.readlines()
dump_data = dump_data[-100:]

with open(f"dump_data", "w") as f:
    f.write("\n".join(dump_data))
# print(dump_data)
# Initialize variables to track timesteps and positions
last_timestep_data = []
current_timestep_data = []
is_reading_atoms = False
current_timestep = None
last_timestep = None

# Extract both the last timestep and the corresponding box size from the dump file
for line_index, line in enumerate(dump_data):
    if "ITEM: TIMESTEP" in line:
        current_timestep = int(dump_data[dump_data.index(line) + 1].strip())
        if current_timestep_data:  # If there's data from the previous timestep
            last_timestep = current_timestep
            last_timestep_data = current_timestep_data.copy()
        current_timestep_data = []
        is_reading_atoms = False
    elif "ITEM: BOX BOUNDS pp pp pp" in line:
        is_reading_atoms = False  # Stop reading atom data temporarily
        # Read the next three lines for box size
        box_bounds = {}
        for i, axis in enumerate(['x', 'y', 'z']):
            bounds = dump_data[dump_data.index(line) + 1 + i].strip().split()
            box_bounds[axis] = [float(bounds[0]), float(bounds[1])]
    elif "ITEM: ATOMS" in line:
        for i in range(1,65):
            if line_index + i < len(dump_data):
                current_timestep_data.append(dump_data[line_index + i].strip())

print(last_timestep_data)

# Calculate the box size vectors for the last timestep
box_size_vectors_last_timestep = {
    'x': box_bounds['x'][1] - box_bounds['x'][0],
    'y': box_bounds['y'][1] - box_bounds['y'][0],
    'z': box_bounds['z'][1] - box_bounds['z'][0]
}

# Correct the mapping extraction from the masses data
element_mapping_corrected = {}
for line in masses_data:
    match_corrected = re.match(r"mass[s]*?(\d+)\s+([\d\.]+)\s+#\s+(\w+)", line.strip())
    if match_corrected:
        type_id_corrected = int(match_corrected.group(1))
        element_corrected = match_corrected.group(3)
        element_mapping_corrected[type_id_corrected] = element_corrected

# Re-process the atom data for the last timestep
atom_data_last_timestep = []
for entry in current_timestep_data:
    parts = entry.split()
    atom_type_id = int(parts[1])
    # Use the corrected mapping to find the element symbol
    element = element_mapping_corrected.get(atom_type_id, "Unknown")
    atom_data_last_timestep.append([element] + parts[2:5])  # Include only element and coordinates

# Create a DataFrame for corrected atom data for the last timestep
df_atoms_last_timestep = pd.DataFrame(atom_data_last_timestep, columns=['Element', 'x', 'y', 'z'])

# Function to convert DataFrame to POSCAR format using extracted box sizes
def convert_to_poscar_with_box(df, box_vectors, filename="POSCAR"):
    # Extract unique elements and count them
    elements = df['Element'].unique()
    element_counts = df['Element'].value_counts()

    # Prepare POSCAR content
    poscar_lines = []

    # Title line
    poscar_lines.append("Generated POSCAR from LAMMPS Dump")

    # Scaling factor
    poscar_lines.append("1.0")

    # Lattice vectors from extracted box sizes
    poscar_lines.append(f"{box_vectors['x']} 0.0 0.0")
    poscar_lines.append(f"0.0 {box_vectors['y']} 0.0")
    poscar_lines.append(f"0.0 0.0 {box_vectors['z']}")

    # Add element symbols and counts
    poscar_lines.append(" ".join(elements))
    poscar_lines.append(" ".join(str(element_counts[el]) for el in elements))

    # Add the coordinate type (Direct or Cartesian)
    poscar_lines.append("Cartesian")


    # Add atomic positions
    for _, row in df.iterrows():
        poscar_lines.append(f"{row['x']} {row['y']} {row['z']}")

    # Write to POSCAR file
    with open(f"{output_file_path}", "w") as f:
        f.write("\n".join(poscar_lines))

    return f"{output_file_path}"

# Convert the corrected DataFrame to POSCAR format using the extracted box sizes
poscar_file_path_final = convert_to_poscar_with_box(df_atoms_last_timestep, box_size_vectors_last_timestep)

poscar_file_path_final





import numpy as np

# Example 'data' array (64 rows and 3 columns)
data = np.random.rand(64, 3)  # Replace with your actual data array

# 'number' array, specifying the number of rows for each sub-array
number = [8, 8, 8, 8, 32]

# Initialize an empty list to store the split arrays
split_data = []

# Variable to keep track of the current index for slicing
start_idx = 0

# Loop through the 'number' array and slice 'data' accordingly
for n in number:
    # Slice the data array based on the current number of rows
    split_data.append(data[start_idx:start_idx + n, :])
    
    # Update the starting index for the next slice
    start_idx += n

# Now, split_data contains 5 arrays, with rows corresponding to the 'number' array
for idx, array in enumerate(split_data):
    print(f"Array {idx + 1} shape: {array.shape}")

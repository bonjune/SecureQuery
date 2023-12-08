import numpy as np

# Function to calculate min, max, and mean for each column
def calculate_statistics(csv_file):
    # Load the CSV file into a numpy array
    data = np.genfromtxt(csv_file, delimiter=',')
    
    # Take the absolute value of the third column
    data[:, 2] = np.abs(data[:, 2])
    
    # Calculate min, max, and mean for each column
    statistics = [(np.min(column), np.max(column), np.mean(column)) for column in data.T]
    
    return statistics

# Provide the path to your CSV file
csv_file_path = 'output_ip.csv'

# Calculate statistics
result = calculate_statistics(csv_file_path)

# Display message
print(f'The third column is the abs() value of Operation Result Difference.')

# Display the results
for i, (min_val, max_val, mean_val) in enumerate(result):
    print(f"Column {i + 1}: Min = {min_val}, Max = {max_val}, Mean = {mean_val}")


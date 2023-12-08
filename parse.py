# Assuming the data is stored in a file named 'data.txt'
input_file_path = 'data_ip.txt'
output_file_path = 'output_ip.csv'

with open(input_file_path, 'r') as file:
  lines = file.readlines()

data = []
current_entry = None

for line in lines:
  if line.startswith("size:"):
    current_entry = {"name": line.split(
      ":")[0].strip(), "size": int(line.split(":")[1].strip())}
  elif line.startswith("unencrypted operation:"):
    current_entry["unencrypted_operation"] = float(
      line.split(":")[1].strip())
  elif line.startswith("encrypted operation:"):
    current_entry["encrypted_operation"] = float(
      line.split(":")[1].strip())
  elif line.startswith("operation result difference:"):
    current_entry["operation_result_difference"] = float(
      line.split(":")[1].strip())
    data.append(current_entry)

with open(output_file_path, 'w') as output_file:
    for entry in data:
      output_file.write(
        f"{entry['name']}, {entry['size']}, {entry['unencrypted_operation']}, {entry['encrypted_operation']}, {entry['operation_result_difference']}\n"
      )
      print(f"{entry['name']}, {entry['size']}, {entry['unencrypted_operation']}, {entry['encrypted_operation']}, {entry['operation_result_difference']}\n")

print(f"Output written to {output_file_path}")

from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import pandas as pd
import struct

# Initialize Pyfhel context
HE = Pyfhel()
HE.contextGen(scheme='bfv', n=2**14, t_bits=20)  # hello world options

def float_to_bytes(f):
    # Pack the float into a binary representation
    bytes_representation = struct.pack('!f', f)
    return bytes_representation

def bytes_to_float(bytes_representation):
    # Unpack the bytes into a float
    unpacked_float = struct.unpack('!f', bytes_representation)
    return unpacked_float[0]

# Load  CSV data
df = pd.read_csv('data.csv')

# Display the original dataset
print("Original Dataset:")
print(df)

# Having a problem with this code block
# if given int or float, wants bytes (TypeError)
# if given bytes, not storeable (BufferError)
'''
# Create a copy of the 'Operating Gross Margin' column as bytes
# Use float_to_bytes to convert each float to a bytes-like object
bytes_column = [float_to_bytes(x) for x in df[' Operating Gross Margin']]

# Encrypt the bytes column
encrypted_column = [HE.encryptInt(int.from_bytes(x, 'big')) for x in bytes_column]

# Encrypt a column from the dataset
encrypted_column = [HE.encryptInt(float_to_bytes(x)) for x in df[' Operating Gross Margin']]
'''

# Perform homomorphic addition on the encrypted column
homomorphic_sum = HE.addMany(encrypted_column)

# Decrypt the result
decrypted_sum = HE.decryptInt(homomorphic_sum)

# Convert the result back to a float
result_float = bytes_to_float(decrypted_sum)

# Display the result
print("\nHomomorphic Sum of Operating Gross Margin:")
print(result_float)
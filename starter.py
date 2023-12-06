from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import pandas as pd
import numpy as np
import struct

# Initialize Pyfhel context
HE = Pyfhel()
HE.contextGen(scheme='ckks', n=2**14, scale=2**30, qi_sizes=[60, 30, 30, 30, 60])

def float_to_bytes(f):
    # Pack the float into a binary representation
    bytes_representation = struct.pack('!f', f)
    return bytes_representation

def bytes_to_float(bytes_representation):
    # Unpack the bytes into a float
    unpacked_float = struct.unpack('!f', bytes_representation)
    return unpacked_float[0]

# Load  CSV data
csv_read = pd.read_csv('data.csv')
unencrypted_data = csv_read.to_numpy(dtype=float)

# Display the original dataset
print("Original Dataset:")
print(csv_read)

'''
Having a problem with this code block
if given float, wants bytes (TypeError)
if given bytes, not storeable (BufferError)
'''
# Encrypt a column from the dataset
#encrypted_column = [HE.encryptFrac(x) for x in csv_read[' Operating Gross Margin']]
#encrypted_column = [HE.encryptFrac(float_to_bytes(x)) for x in csv_read[' Operating Gross Margin']]
'''
Alternatively, pandas to numpy can be done column by column.
'''
encrypted_column = [HE.encryptFrac(x) for x in unencrypted_data[' Operating Gross Margin']]

# Perform homomorphic addition on the encrypted column
homomorphic_sum = HE.addMany(encrypted_column)

# Decrypt the result
decrypted_sum = HE.decryptInt(homomorphic_sum)

# Convert the result back to a float
result_float = bytes_to_float(decrypted_sum)

# Display the result
print("\nHomomorphic Sum of Operating Gross Margin:")
print(result_float)

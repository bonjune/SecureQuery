from Pyfhel import Pyfhel
import pandas as pd
import numpy as np


# Initialize Pyfhel context
def init():
    HE = Pyfhel()
    HE.contextGen(scheme="ckks", n=2**14, scale=2**30, qi_sizes=[60, 30, 30, 30, 60])
    HE.keyGen()
    HE.rotateKeyGen()

    return HE


HE = init()
data = pd.read_csv("data.csv")

ogm = data[" Operating Gross Margin"].to_numpy(dtype=np.float32, copy=True)

ogm_sum = ogm.sum()

ogm_holder = HE.encrypt(0.0)
for record in ogm:
    ogm_holder += HE.encrypt(record)
ogm_sum_cipher = ogm_holder
ogm_sum_dec = ogm_sum_cipher.decrypt()

print(ogm_sum)
print(ogm_sum_dec)

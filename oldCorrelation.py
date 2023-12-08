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


def main():
    HE = init()
    data = pd.read_csv("data.csv")

    ogm = data[" Operating Gross Margin"].to_numpy(dtype=np.float32, copy=True)
    ogm_sum = ogm.sum()

    ogm_holder = HE.encrypt(0.0)
    records = 0
    for record in ogm:
        ogm_holder += HE.encrypt(record)
        records += 1
    ogm_sum_c = ogm_holder
    ogm_mean_c = ogm_sum_c / records
    ogm_op_dec = ogm_mean_c.decrypt()

    print(ogm_op_dec)
    print(ogm_sum / records)
    return 0


main()

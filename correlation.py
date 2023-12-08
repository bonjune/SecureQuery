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


def mean(HE, data_vec):
    data_holder = HE.encrypt(0.0)
    records = 0
    for record in data_vec:
        data_holder += HE.encrypt(record)
        records += 1
    data_sum_c = data_holder
    data_mean_c = data_sum_c / records
    return data_mean_c


def main():
    HE = init()
    data = pd.read_csv("data.csv")

    ogm = data[" Operating Gross Margin"].to_numpy(dtype=np.float32, copy=True)

    # call mean
    ogm_mean_c = mean(HE, ogm)
    # decrypt mean
    ogm_op_dec = ogm_mean_c.decrypt()

    print(ogm_op_dec[0])
    return 0


if __name__ == "__main__":
    main()

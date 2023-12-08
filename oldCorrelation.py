from Pyfhel import Pyfhel
from Pyfhel import PyCtxt
import pandas as pd
import numpy as np


# Initialize Pyfhel context
def init():
    HE = Pyfhel()
    HE.contextGen(scheme="ckks", n=2**14, scale=2**30, qi_sizes=[60, 30, 30, 30, 60])
    HE.keyGen()
    HE.rotateKeyGen()

    return HE


def cipher_sum(ctxt: PyCtxt, size: int):
    if size <= 1:
        return ctxt

    fold = size // 2
    if size % 2 == 0:
        return cipher_sum(ctxt + (ctxt << fold), fold)

    hold = ctxt.copy()
    return (hold << (size - 1)) + cipher_sum(ctxt + (ctxt << fold), fold)


def mean(HE, data_vec):
    data_sum_c = cipher_sum(data_vec, len(data_vec))
    data_mean_c = data_sum_c / len(data_vec)
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

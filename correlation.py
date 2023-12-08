import pandas as pd
import numpy as np
import glob
from hashlib import sha256

from Pyfhel import Pyfhel as FHE, PyCtxt


enc_data = {}


# Initialize the CKKS FHE context
def init() -> FHE:
    HE = FHE()
    HE.contextGen(scheme="ckks", n=2**14, scale=2**30, qi_sizes=[60, 30, 30, 30, 60])
    HE.keyGen()
    HE.relinKeyGen()
    HE.rotateKeyGen()

    HE.save_context('ckks-context')
    HE.save_public_key('ckks-pubkey')
    HE.save_secret_key('ckks-seckey')
    HE.save_relin_key('ckks-relinkey')
    HE.save_rotate_key('ckks-rotate-key')

    return HE


def init_scheme():
    ckks_settings = glob.glob('ckks-*')
    if len(ckks_settings) == 5:
        HE = FHE()
        HE.load_context('ckks-context')
        HE.load_public_key('ckks-pubkey')
        HE.load_secret_key('ckks-seckey')
        HE.load_relin_key('ckks-relinkey')
        HE.load_rotate_key('ckks-rotate-key')
    else:
        HE = init()

    return HE


def cipher_sum(ctxt: PyCtxt, size: int):
    if size <= 1:
        return ctxt

    fold = size // 2
    if size % 2 == 0:
        return cipher_sum(ctxt + (ctxt << fold), fold)

    hold = ctxt.copy()
    return (hold << (size - 1)) + cipher_sum(ctxt + (ctxt << fold), fold)


def cipher_average(ctxt: PyCtxt, size: int):
    avg_cipher = cipher_sum(ctxt, size) / size
    return avg_cipher


def cipher_inner_product(ctxt1: PyCtxt, ctxt2: PyCtxt, size: int):
    ctxt_mul = ~(ctxt1 * ctxt2)
    return cipher_sum(ctxt_mul, size)


def cipher_covariance(ctxt1: PyCtxt, ctxt2: PyCtxt, size: int):
    cmean1 = cipher_average(ctxt1, size)
    cmean2 = cipher_average(ctxt2, size)

    return cipher_inner_product(ctxt1 - cmean1, ctxt2 - cmean2, size) / size


def cipher_std_dev(ctxt: PyCtxt, size: int):
    cmean = cipher_average(ctxt, size)
    dev = ~(ctxt - cmean)**2
    std_dev = (cipher_sum(dev / (size - 1), size)) ** 0.5
    return std_dev


def cipher_corr(ctxt1: PyCtxt, ctxt2: PyCtxt):
    ctxt_mul = ctxt1 * ctxt2
    return cipher_sum(ctxt_mul)


def query(col_name: str, f: str | None = None):
    print(col_name)
    global enc_data
    hashed_col_name = sha256(col_name.encode()).hexdigest()
    ctxt, size = enc_data[hashed_col_name]
    hashed_col_name2 = sha256(col_name.encode()).hexdigest()
    ctxt2, size = enc_data[hashed_col_name2]
    a = cipher_covariance(ctxt, ctxt2, size).decrypt()[0]
    a = cipher_std_dev(ctxt, size).decrypt()[0]
    '''
    a = cipher_sum(ctxt, size).decrypt()[0]
    '''
    return a


def main():
    HE = init_scheme()
    data = pd.read_csv("data.csv")

    global enc_data

    for col_name in data.columns:
        hashed_col_name = sha256(col_name.encode()).hexdigest()
        col_data = data[col_name].to_numpy(copy=True)
        data_ctxt = HE.encrypt(col_data)
        enc_data[hashed_col_name] = (data_ctxt, len(col_data))

    #ogm_dec = query(" Operating Gross Margin")
    ogm_dec = query(" Operating Gross Margin", " Operating Profit Rate")
    print('decrypted', ogm_dec)
    data[" Operating Gross Margin"].mean()

    return 0


if __name__ == "__main__":
    main()

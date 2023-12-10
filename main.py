from cipher_operations import (
    init_scheme, hash_column_name, encrypted_data,
    cipher_average, cipher_sum, cipher_inner_product
)
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


def query_sum(col_name: str, f: str | None = None):
    print(col_name, " summation")
    global enc_data
    hashed_col_name = sha256(col_name.encode()).hexdigest()
    ctxt, size = enc_data[hashed_col_name]
    hashed_col_name2 = sha256(col_name.encode()).hexdigest()
    ctxt2, size = enc_data[hashed_col_name2]
    a = cipher_sum(ctxt, size).decrypt()[0]
    return a


def query_average(col_name: str, f: str | None = None):
    print(col_name, " average")
    global enc_data
    hashed_col_name = sha256(col_name.encode()).hexdigest()
    ctxt, size = enc_data[hashed_col_name]
    hashed_col_name2 = sha256(col_name.encode()).hexdigest()
    ctxt2, size = enc_data[hashed_col_name2]
    a = cipher_average(ctxt, size).decrypt()[0]
    return a


def query_ip(col_name: str, f: str | None = None):
    print(col_name, " inner product")
    global enc_data
    hashed_col_name = sha256(col_name.encode()).hexdigest()
    ctxt, size = enc_data[hashed_col_name]
    hashed_col_name2 = sha256(col_name.encode()).hexdigest()
    ctxt2, size = enc_data[hashed_col_name2]
    a = cipher_inner_product(ctxt, ctxt, size).decrypt()[0]
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

    ogm_sum = query_sum(" Operating Gross Margin")
    print('decrypted', ogm_sum)
    print('expected', data[" Operating Gross Margin"].sum())

    ogm_avg = query_average(" Operating Gross Margin")
    print('decrypted', ogm_avg)
    print('expected', data[" Operating Gross Margin"].mean())

    ogm_ip = query_ip(" Operating Gross Margin")
    print('decrypted', ogm_ip)
    ip_expected = np.dot(data[" Operating Gross Margin"], data[" Operating Gross Margin"])
    print('expected', ip_expected)

    return 0


if __name__ == "__main__":
    main()

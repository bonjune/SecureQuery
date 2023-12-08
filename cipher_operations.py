from Pyfhel import Pyfhel, PyCtxt
import glob
from hashlib import sha256
import pandas as pd


def init_scheme():
    ckks_settings = glob.glob("ckks-*")
    if len(ckks_settings) == 5:
        HE = Pyfhel()
        HE.load_context("ckks-context")
        HE.load_public_key("ckks-pubkey")
        HE.load_secret_key("ckks-seckey")
        HE.load_relin_key("ckks-relinkey")
        HE.load_rotate_key("ckks-rotate-key")
    else:
        HE = Pyfhel()
        HE.contextGen(
            scheme="ckks", n=2**14, scale=2**30, qi_sizes=[60, 30, 30, 30, 60]
        )
        HE.keyGen()
        HE.relinKeyGen()
        HE.rotateKeyGen()

        HE.save_context("ckks-context")
        HE.save_public_key("ckks-pubkey")
        HE.save_secret_key("ckks-seckey")
        HE.save_relin_key("ckks-relinkey")
        HE.save_rotate_key("ckks-rotate-key")

    return HE


def hash_column_name(name: str):
    return sha256(name.encode()).hexdigest()


def encrypted_data(encryptor: Pyfhel, data: pd.DataFrame):
    enc_data = {}

    for col_name in data.columns:
        hashed_col_name = hash_column_name(col_name)
        col_data = data[col_name].to_numpy(copy=True)
        data_ctxt = encryptor.encrypt(col_data)
        enc_data[hashed_col_name] = (data_ctxt, len(col_data))

    return enc_data


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
    if ctxt1 is ctxt2:
        ctxt2 = ctxt1.copy()
    ctxt_mul = ~(ctxt1 * ctxt2)  # relinearization to reduce size
    return cipher_sum(ctxt_mul, size)


def cipher_covariance(ctxt1: PyCtxt, ctxt2: PyCtxt, size: int):
    x_mean = cipher_average(ctxt1, size)
    y_mean = cipher_average(ctxt2, size)

    return cipher_inner_product(ctxt1 - x_mean, ctxt2 - y_mean, size) / size

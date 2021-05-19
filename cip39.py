# coding: utf-8
import itertools
import math
import os

from mnemonic import Mnemonic
from reedsolo import RSCodec

BIP39_SYMBOL_SIZE=11

def validate_n_k(n, k):
    if n % 3 != 0 or k % 3 != 0:
        return False, "n and k must be divisible by 3"

    if n < 12 or n > 24 or k < 0 or (n-k) < 12:
        return False,  "n at most 24 and at least 12. k must be at least 0 and n-k must be at least 12."

    return True, None

def random_bits(bits):
    data = os.urandom(math.ceil(bits / 8))
    # Turn random bytes into binary string encoding and return.
    return ''.join(bin(byte)[2:].zfill(8) for byte in data)[:bits]

def bits_to_symbols(bits, size=BIP39_SYMBOL_SIZE):
    if len(bits) % size != 0:
        raise ValueError(f"bits cannot be evenly divided into symbols of size {size}")

    return [int(bits[i*size:(i+1)*size], 2) for i in range(len(bits)//size)]

def symbols_to_mnemonic(symbols, mnemonic):
    return ' '.join(mnemonic.wordlist[s] for s in symbols)

def mnemonic_to_symbols(phrase, mnemonic):
    words = phrase.split(' ')
    symbols = [-1] * len(words)
    for i, word in enumerate(words):
        if word not in mnemonic.wordlist:
            continue

        symbols[i] = mnemonic.wordlist.index(word)

    return symbols

def generate(n, k=3, mnemonic=Mnemonic("english")):
    """generate a mnemonic phrase with the specified level of error correction

    Arguments:
        n (int): Total number of words in the phrase.
        k (int): Number of words devoted to error correction.
        mnemonic (Mnemonic): Istance of Mnemonic to use.
    """
    ok, error = validate_n_k(n, k)
    if not ok:
        raise ValueError(error)

    coder = RSCodec(nsize=n, nsym=k, c_exp=BIP39_SYMBOL_SIZE)
    for i in itertools.count():
        bits = random_bits((n-k)*BIP39_SYMBOL_SIZE)
        symbols = bits_to_symbols(bits, BIP39_SYMBOL_SIZE)
        coded = coder.encode(symbols)
        phrase = symbols_to_mnemonic(coded, mnemonic)
        if not mnemonic.check(phrase):
            continue

        return phrase

def recover(phrase, n, k, mnemonic=Mnemonic("english")):
    ok, error = validate_n_k(n, k)
    if not ok:
        raise ValueError(error)

    symbols = mnemonic_to_symbols(phrase, mnemonic)
    if len(symbols) != n:
        raise ValueError("number of words in mnemonic must match n")

    coder = RSCodec(nsize=n, nsym=k, c_exp=BIP39_SYMBOL_SIZE)
    erasures = [i for i, s in enumerate(symbols) if s < 0]
    recovered, _, _ = coder.decode(symbols, erase_pos=erasures)
    coded = coder.encode(recovered)
    return symbols_to_mnemonic(coded, mnemonic)

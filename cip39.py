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

    if n < 12 or n > 24:
        return False, "n must be at least 12 and at most 24"

    if k < 12 or k > n:
        return False, "k must be at least 12 and at most n"

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
    words = phrase.split()
    symbols = [-1] * len(words)
    for i, word in enumerate(words):
        if word not in mnemonic.wordlist:
            continue

        symbols[i] = mnemonic.wordlist.index(word)

    return symbols

def generate(n, k=12, mnemonic=Mnemonic("english")):
    """Generate a mnemonic phrase with the specified level of error correction.

    Phrases include t=(n-k) "error correcting" words, allowing the correction of up to t invalid
    words in a phrase, and up to floor(t/2) words that are wrong, but still valid BIP-39 words.

    Arguments:
        n (int): Total number of words in the phrase.
        k (int): Number of words chosen at random.
        mnemonic (Mnemonic): Instance of Mnemonic to use.
    """
    ok, error = validate_n_k(n, k)
    if not ok:
        raise ValueError(error)

    coder = RSCodec(nsize=n, nsym=(n-k), c_exp=BIP39_SYMBOL_SIZE)
    for i in itertools.count():
        bits = random_bits(k*BIP39_SYMBOL_SIZE)
        symbols = bits_to_symbols(bits, BIP39_SYMBOL_SIZE)
        coded = coder.encode(symbols)
        phrase = symbols_to_mnemonic(coded, mnemonic)
        if not mnemonic.check(phrase):
            continue

        return phrase

def recover(phrase, k=12, mnemonic=Mnemonic("english")):
    """Attempts to recover the original mnemonic phrase from a mnemonic phrase with errors.

    Infers the value of n from the number of words in the phrase. If words are missing or unknown,
    include an arbitrary character in its place. (e.g. '_')

    Arguments:
        phrase (str): Mnemonic phrase with errors to fix.
        k (int): Number of words chosen at random.
        mnemonic (Mnemonic): Instance of Mnemonic to use.
    """
    symbols = mnemonic_to_symbols(phrase, mnemonic)
    ok, error = validate_n_k(len(symbols), k)
    if not ok:
        raise ValueError(error)

    coder = RSCodec(nsize=len(symbols), nsym=(len(symbols)-k), c_exp=BIP39_SYMBOL_SIZE)
    erasures = [i for i, s in enumerate(symbols) if s < 0]
    recovered, _, _ = coder.decode(symbols, erase_pos=erasures)
    coded = coder.encode(recovered)
    phrase = symbols_to_mnemonic(coded, mnemonic)

    if not mnemonic.check(phrase):
        raise ValueError("error-corrected phrase does not have a valid checksum")

    return phrase

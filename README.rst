CIP39
=====

In this repository is a reference implementation for the proposed CIP39 standard, an extension to the `BIP39 <https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki>`_ standard for mnemonic wallet encoding.

CIP39 extends, with full backwards compatibility, the BIP39 standard to include up error correction such that words can misspelled, swapped positions, or otherwise lost without losing the encoded secret. Within phrases of length 12 to 24 words, it supports the replacement of 0 to 12 random words with error correction words. For every error correction word used, up to one word can be lost at a known position (e.g. by misspelling), and with every two error correction words, up to one word can be corrected at an unknown position (e.g. by swapping two words).

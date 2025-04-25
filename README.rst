CIP-39
======

In this repository is a proof-of-concept implementation for the proposed `CIP-39 standard <https://github.com/celo-org/celo-proposals/blob/master/CIPs/cip-0039.md>`_, a backwards-compatible extension to the `BIP-39 <https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki>`_ standard for mnemonic wallet encoding.

CIP-39 extends, with full backwards compatibility, the BIP-39 standard to include up error correction such that words can misspelled, swapped positions, or otherwise lost without losing the encoded secret. Within phrases of length 12 to 24 words, it supports the replacement of 0 to 12 random words with error correction words. For every error correction word used, up to one word can be lost at a known position (e.g. by misspelling), and with every two error correction words, up to one word can be corrected at an unknown position (e.g. by swapping two words).

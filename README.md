# Cipher Tools in Python

This repository contains multiple classic cipher implementations with graphical user interfaces (GUIs) built using Tkinter.

## Files Overview

| File         | Description                                               |
|--------------|-----------------------------------------------------------|
| `ADFGVX.py`  | ADFG(V)X cipher with matrix size and language selection   |
| `affine.py`  | Affine cipher (requires keys `a` and `b`)                 |
| `playfair.py`| Playfair cipher with CZ/EN mode switch                    |
| `rsa.py`     | RSA encryption and decryption tool                        |
| `dsa.py`     | Digital signature using RSA and SHA3-512                  |

## ▶How to Run

1. **Install Python 3** (if not already installed):  
   [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Install required libraries** (only needed for some tools):
   ```bash
   pip install pyperclip unidecode

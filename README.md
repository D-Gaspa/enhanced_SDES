# Enhanced Simplified Data Encryption Standard (Enhanced S-DES)

## Overview

This project implements an Enhanced version of the Simplified Data Encryption Standard (S-DES) algorithm.
The Enhanced S-DES combines the original S-DES with additional security layers,
including columnar transposition and shift rows operations, to create a more robust encryption scheme.

The main goals of this project are:

1. To implement the basic S-DES algorithm
2. To enhance its security by adding pre-processing steps
3. To provide a flexible and user-friendly interface for encryption and decryption

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Algorithm Details](#algorithm-details)
    - [S-DES](#s-des)
    - [Columnar Transposition](#columnar-transposition)
    - [Shift Rows](#shift-rows)
    - [Enhanced S-DES Process](#enhanced-s-des-process)

## Installation

To use this project, clone the repository and ensure you have a Python environment set up:

```bash
git clone https://github.com/D-Gaspa/enhanced_SDES.git
cd enhanced-sdes
```

No additional dependencies are required.

## Usage

To run the Enhanced S-DES encryption system, execute the `main.py` script:

```bash
python main.py
```

This will launch an interactive command-line interface with the following options:

1. Encrypt a message
2. Decrypt a message
3. Exit the program

When encrypting or decrypting, you'll be prompted to:

- Enter the message
- Provide or generate an S-DES key
- Provide or generate a transposition key
- Specify the number of transposition rounds
- Choose whether to display the encryption/decryption progress

Example session:

```
Welcome to the Enhanced S-DES Encryption System!

Enter 1 to encrypt, 2 to decrypt, or 3 to exit: 1
Enter the message to encrypt: WARNING WE WERE COMPROMISED
Enter the 10-bit S-DES key (or press Enter to generate): 
Generated S-DES key: 1110111000
Enter the transposition key (space/comma-separated or [list] format, or press Enter to generate): 
Enter column size (2-26, or press Enter for default): 3
Generated transposition key: [1, 3, 2]
Enter the number of transposition rounds (or press Enter for default 2): 5
Show encryption progress? (y/n): y
Encrypting ...

Columnar Transposition: WDPEREAWSMWRIIEEMCNOONGR
Shift Rows: WDPREESAWMWRIIEEMCNOONGR
S-DES Encryption: 11045829E3E374A2113F1129BABAE3E33F9FE11414E11A29

Encrypted message (hex): 11045829E3E374A2113F1129BABAE3E33F9FE11414E11A29

Enter 1 to encrypt, 2 to decrypt, or 3 to exit: 2
Use saved encryption info? (y/n): y
Enter the message to decrypt (hex): 11045829E3E374A2113F1129BABAE3E33F9FE11414E11A29
Show decryption progress? (y/n): y
Decrypting ...

S-DES Decryption: WDPREESAWMWRIIEEMCNOONGR
Inverse Shift Rows: WDPEREAWSMWRIIEEMCNOONGR
Decrypted message: WARNINGWEWERECOMPROMISED

Enter 1 to encrypt, 2 to decrypt, or 3 to exit: 3
Exiting the program. Goodbye!
```

## Algorithm Details

### S-DES

The Simplified Data Encryption Standard (S-DES) is a block cipher that operates on 8-bit blocks of plaintext using a
10-bit key.
It involves:

1. Initial Permutation (IP)
2. Two rounds of a complex function fK, involving:
    - Expansion/Permutation (E/P)
    - XOR with a round key
    - S-box substitutions
    - 4-bit permutation (P4)
3. Switch function (SW)
4. Inverse Initial Permutation (IP^-1)

### Columnar Transposition

The columnar transposition technique rearranges the characters of the plaintext:

1. Arrange the plaintext in rows of a matrix
2. Read out the characters in a column order specified by the key
3. Can and should be applied multiple times for increased security

### Shift Rows

The shift rows operation performs a cyclic shift on the rows of the input:

1. First row: no shift
2. Second row: shift one position left
3. Third row: shift two positions left
4. (Pattern continues for larger matrices)

### Enhanced S-DES Process

Encryption:

1. Apply Columnar Transposition (multiple rounds if specified)
2. Perform Shift Rows operation
3. Convert to binary
4. Apply S-DES encryption
5. Convert the result to hexadecimal

Decryption:

1. Convert hexadecimal to binary
2. Apply S-DES decryption
3. Convert to text
4. Perform inverse Shift Rows operation
5. Apply inverse Columnar Transposition (multiple rounds if used in encryption)

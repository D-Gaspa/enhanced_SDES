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
3. Change progress level
4. Exit the program

When encrypting or decrypting, you'll be prompted to:

- Enter the message
- Provide or generate an S-DES key
- Provide or generate a transposition key
- Specify the number of transposition rounds
- Choose the progress level (0: None, 1: Normal, 2: Detailed)

Example session:

```
Welcome to the Enhanced S-DES Encryption System!

Enter 1 to encrypt, 2 to decrypt, 3 to change progress level, or 4 to exit: 3
Enter progress level (0: None, 1: Normal, 2: Detailed): 2
Progress level set to: DETAILED

Enter 1 to encrypt, 2 to decrypt, 3 to change progress level, or 4 to exit: 1
Enter the message to encrypt: Warning! We are compromised
Enter the 10-bit S-DES key (or press Enter to generate): 
Generated S-DES key: 1010100110
Enter the transposition key (space/comma-separated or [list] format, or press Enter to generate): 
Enter column size (2-26, or press Enter for default 3): 5
Generated transposition key: [4, 3, 2, 1, 5]
Enter the number of transposition rounds (or press Enter for default 2): 4
Plaintext: Warning! We are compromised

Initial Table:
+---------+---------+---------+---------+---------+
| Col 1   | Col 2   | Col 3   | Col 4   | Col 5   |
+=========+=========+=========+=========+=========+
| W       | a       | r       | n       | i       |
+---------+---------+---------+---------+---------+
| n       | g       | !       |         | W       |
+---------+---------+---------+---------+---------+
| e       |         | a       | r       | e       |
+---------+---------+---------+---------+---------+
|         | c       | o       | m       | p       |
+---------+---------+---------+---------+---------+
| r       | o       | m       | i       | s       |
+---------+---------+---------+---------+---------+
| e       | d       |         |         |         |
+---------+---------+---------+---------+---------+
After round 1:
+---------+---------+---------+---------+---------+
| Col 1   | Col 2   | Col 3   | Col 4   | Col 5   |
+=========+=========+=========+=========+=========+
| n       |         | r       | m       | i       |
+---------+---------+---------+---------+---------+
|         | r       | !       | a       | o       |
+---------+---------+---------+---------+---------+
| m       |         | a       | g       |         |
+---------+---------+---------+---------+---------+
| c       | o       | d       | W       | n       |
+---------+---------+---------+---------+---------+
| e       |         | r       | e       | i       |
+---------+---------+---------+---------+---------+
| W       | e       | p       | s       |         |
+---------+---------+---------+---------+---------+

[... more rounds of transposition ...]

Columnar Transposition: "n rmoir!a m agnco Wie rdWepse "

Before Shift:
+---------+---------+---------+---------+---------+
| Col 1   | Col 2   | Col 3   | Col 4   | Col 5   |
+=========+=========+=========+=========+=========+
| n       |         | r       | m       | o       |
+---------+---------+---------+---------+---------+
| i       | r       | !       | a       |         |
+---------+---------+---------+---------+---------+
| m       |         | a       | g       | n       |
+---------+---------+---------+---------+---------+
| c       | o       |         | W       | i       |
+---------+---------+---------+---------+---------+
| e       |         | r       | d       | W       |
+---------+---------+---------+---------+---------+
| e       | p       | s       | e       |         |
+---------+---------+---------+---------+---------+
After Shift:
+---------+---------+---------+---------+---------+
| Col 1   | Col 2   | Col 3   | Col 4   | Col 5   |
+=========+=========+=========+=========+=========+
| n       |         | r       | m       | o       |
+---------+---------+---------+---------+---------+
| r       | !       | a       |         | i       |
+---------+---------+---------+---------+---------+
| a       | g       | n       | m       |         |
+---------+---------+---------+---------+---------+
| W       | i       | c       | o       |         |
+---------+---------+---------+---------+---------+
| W       | e       |         | r       | d       |
+---------+---------+---------+---------+---------+
| e       | p       | s       | e       |         |
+---------+---------+---------+---------+---------+

Shift Rows: "n rmor!a iagnm Wico We rdepse "

Converted to binary: 0110111000100000011100100110110101101111...(200 more characters)

Encrypting with S-DES:
Total blocks to process: 30
Key: 1010100110

Encrypting block 1/30
Input block: 01101110
Subkey generation:
  Original key: 1010100110
  After P10: 1100001110
  After LS-1: 1000111100
  Subkey 1: 10101100
  After LS-2: 0011010011
  Subkey 2: 11010011
Subkey 1: 10101100
Subkey 2: 11010011
After initial permutation: 11100011
  Round input: L=1110, R=0011
  Expanded R: 10010110
  After XOR with subkey: 00111010
  After S-boxes: 1000
  After P4: 0001
  Round output: 11110011
After first round: 11110011
After switch: 00111111
  Round input: L=0011, R=1111
  Expanded R: 11111111
  After XOR with subkey: 00101100
  After S-boxes: 0001
  After P4: 0100
  Round output: 01111111
After second round: 01111111
Final output: 10111111
Output block: 10111111
Current result: 10111111

[... more blocks encrypted ...]

Final encrypted result: 1011111110001011011101111010111101101010...(200 more characters)

Encrypted message (hex): BF8B77AF6A77C4D08BEAD044BFAF8B0AEA016A8B0A558B777A558EE7558B

Enter 1 to encrypt, 2 to decrypt, 3 to change progress level, or 4 to exit: 2
Use saved encryption info? (y/n): y
Enter the message to decrypt (hex): BF8B77AF6A77C4D08BEAD044BFAF8B0AEA016A8B0A558B777A558EE7558B
Ciphertext: BF8B77AF6A77C4D08BEAD044BFAF8B0AEA016A8B0A558B777A558EE7558B

Converted to binary: 1011111110001011011101111010111101101010...(200 more characters)

Decrypting with S-DES:
Total blocks to process: 30
Key: 1010100110

Decrypting block 1/30
Input block: 10111111
Subkey generation:
  Original key: 1010100110
  After P10: 1100001110
  After LS-1: 1000111100
  Subkey 1: 10101100
  After LS-2: 0011010011
  Subkey 2: 11010011
Subkey 1: 10101100
Subkey 2: 11010011
After initial permutation: 01111111
  Round input: L=0111, R=1111
  Expanded R: 11111111
  After XOR with subkey: 00101100
  After S-boxes: 0001
  After P4: 0100
  Round output: 00111111
After first round: 00111111
After switch: 11110011
  Round input: L=1111, R=0011
  Expanded R: 10010110
  After XOR with subkey: 00111010
  After S-boxes: 1000
  After P4: 0001
  Round output: 11100011
After second round: 11100011
Final output: 01101110
Output block: 01101110
Current result: 01101110

[... more blocks decrypted ...]

S-DES Decryption (binary): 0110111000100000011100100110110101101111...(200 more characters)

Converted to text: "n rmor!a iagnm Wico We rdepse "
Before Inverse Shift:
+---------+---------+---------+---------+---------+
| Col 1   | Col 2   | Col 3   | Col 4   | Col 5   |
+=========+=========+=========+=========+=========+
| n       |         | r       | m       | o       |
+---------+---------+---------+---------+---------+
| r       | !       | a       |         | i       |
+---------+---------+---------+---------+---------+
| a       | g       | n       | m       |         |
+---------+---------+---------+---------+---------+
| W       | i       | c       | o       |         |
+---------+---------+---------+---------+---------+
| W       | e       |         | r       | d       |
+---------+---------+---------+---------+---------+
| e       | p       | s       | e       |         |
+---------+---------+---------+---------+---------+
After Inverse Shift:
+---------+---------+---------+---------+---------+
| Col 1   | Col 2   | Col 3   | Col 4   | Col 5   |
+=========+=========+=========+=========+=========+
| n       |         | r       | m       | o       |
+---------+---------+---------+---------+---------+
| i       | r       | !       | a       |         |
+---------+---------+---------+---------+---------+
| m       |         | a       | g       | n       |
+---------+---------+---------+---------+---------+
| c       | o       |         | W       | i       |
+---------+---------+---------+---------+---------+
| e       |         | r       | d       | W       |
+---------+---------+---------+---------+---------+
| e       | p       | s       | e       |         |
+---------+---------+---------+---------+---------+

Inverse Shift Rows: "n rmoir!a m agnco Wie rdWepse "

Initial Table:
+---------+---------+---------+---------+---------+
| Col 1   | Col 2   | Col 3   | Col 4   | Col 5   |
+=========+=========+=========+=========+=========+
| n       |         | r       | m       | o       |
+---------+---------+---------+---------+---------+
| i       | r       | !       | a       |         |
+---------+---------+---------+---------+---------+
| m       |         | a       | g       | n       |
+---------+---------+---------+---------+---------+
| c       | o       |         | W       | i       |
+---------+---------+---------+---------+---------+
| e       |         | r       | d       | W       |
+---------+---------+---------+---------+---------+
| e       | p       | s       | e       |         |
+---------+---------+---------+---------+---------+

[... more rounds of inverse transposition ...]

After round 4:
+---------+---------+---------+---------+---------+
| Col 1   | Col 2   | Col 3   | Col 4   | Col 5   |
+=========+=========+=========+=========+=========+
| W       | a       | r       | n       | i       |
+---------+---------+---------+---------+---------+
| n       | g       | !       |         | W       |
+---------+---------+---------+---------+---------+
| e       |         | a       | r       | e       |
+---------+---------+---------+---------+---------+
|         | c       | o       | m       | p       |
+---------+---------+---------+---------+---------+
| r       | o       | m       | i       | s       |
+---------+---------+---------+---------+---------+
| e       | d       |         |         |         |
+---------+---------+---------+---------+---------+
Decrypted message: Warning! We are compromised

Enter 1 to encrypt, 2 to decrypt, 3 to change progress level, or 4 to exit: 4
Exiting the program. Goodbye!
```

This example demonstrates the detailed progress level (2), showing the step-by-step process of encryption,
including the columnar transposition, shift rows operation, and S-DES encryption for the first block.
The output for the remaining blocks is similar and has been omitted for brevity.

You can adjust the progress level to 1 (Normal) for less detailed output or 0 (None) for minimal output.

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

"""
This module implements the Enhanced Simplified Data Encryption Standard (Enhanced S-DES).

It provides a class that combines the S-DES algorithm with additional security layers,
including columnar transposition and shift rows operations, to create a more robust
encryption scheme.
"""

from typing import List

from core.column_transposition import ColumnTransposition
from core.sdes import SDES
from core.shift_rows import ShiftRows
from utils.key_manager import KeyManager
from utils.progress_level import ProgressLevel
from utils.utilities import Utilities


class EnhancedSDES:
    """
    A class implementing the Enhanced Simplified Data Encryption Standard.

    This class combines the S-DES algorithm with columnar transposition and
    shift rows operations to provide a more secure encryption scheme.

    Attributes:
        progress_level: The level of detail to show during encryption/decryption.
        transposition:  An instance of ColumnTransposition.
        shift_rows:     An instance of ShiftRows.
        sdes:           An instance of SDES.
        key_manager:    An instance of KeyManager.
    """

    def __init__(self):
        """
        Initialize the EnhancedSDES instance.

        """
        self.progress_level = ProgressLevel.NONE
        self.transposition = ColumnTransposition()
        self.shift_rows = ShiftRows()
        self.sdes = SDES()
        self.key_manager = KeyManager()

    def set_progress_level(self, level: ProgressLevel) -> None:
        """
        Set the progress level for the Enhanced S-DES algorithm and its components.

        Args:
            level: The progress level to set.
        """
        self.progress_level = level
        self.transposition.set_progress_level(level)
        self.shift_rows.set_progress_level(level)
        self.sdes.set_progress_level(level)

    def encrypt(self, plaintext: str, sdes_key: str, trans_key: List[int], rounds: int) -> str:
        """
        Encrypt the plaintext using the Enhanced S-DES algorithm.

        Args:
            plaintext:  The text to be encrypted.
            sdes_key:   A 10-bit binary string used as the S-DES key.
            trans_key:  A list of integers representing the transposition key.
            rounds:     The number of rounds for columnar transposition.

        Returns:
            The encrypted ciphertext.
        """
        if self.progress_level != ProgressLevel.NONE:
            print(f"Plaintext: {plaintext}\n")

        # Step 1: Columnar Transposition
        transposed = self.transposition.transpose(plaintext, trans_key, rounds)
        if self.progress_level != ProgressLevel.NONE:
            print(f"\nColumnar Transposition: \"{transposed}\"")

        # Step 2: Shift Rows
        shifted = self.shift_rows.shift(transposed, len(trans_key))
        if self.progress_level != ProgressLevel.NONE:
            print(f"\nShift Rows: \"{shifted}\"")

        # Step 3: S-DES Encryption
        binary = Utilities.text_to_binary(shifted)
        if self.progress_level != ProgressLevel.NONE:
            print(f"\nConverted to binary: {binary}")

        encrypted_binary = self._apply_sdes(binary, sdes_key, encrypt=True)

        cipher_text = Utilities.binary_to_hex(encrypted_binary)

        if self.progress_level != ProgressLevel.NONE:
            print(f"\nS-DES Encryption (hex): {cipher_text}\n")

        return cipher_text

    def decrypt(self, ciphertext: str, sdes_key: str, trans_key: List[int], rounds: int) -> str:
        """
        Decrypt the ciphertext using the Enhanced S-DES algorithm.

        Args:
            ciphertext: The text to be decrypted.
            sdes_key:   A 10-bit binary string used as the S-DES key.
            trans_key:  A list of integers representing the transposition key.
            rounds:     The number of rounds for columnar transposition.

        Returns:
            The decrypted plaintext.
        """
        if self.progress_level != ProgressLevel.NONE:
            print(f"Ciphertext: {ciphertext}")

        # Step 1: S-DES Decryption
        binary = Utilities.hex_to_binary(ciphertext)
        if self.progress_level != ProgressLevel.NONE:
            print(f"\nConverted to binary: {binary}")

        decrypted_binary = self._apply_sdes(binary, sdes_key, encrypt=False)
        if self.progress_level != ProgressLevel.NONE:
            print(f"\nS-DES Decryption (binary): {decrypted_binary}")

        text = Utilities.binary_to_text(decrypted_binary)
        if self.progress_level != ProgressLevel.NONE:
            print(f"\nConverted to text: \"{text}\"")

        # Step 2: Inverse Shift Rows
        unshifted = self.shift_rows.inverse_shift(text, len(trans_key))
        if self.progress_level != ProgressLevel.NONE:
            print(f"\nInverse Shift Rows: \"{unshifted}\"\n")

        # Step 3: Inverse Columnar Transposition
        plaintext = self.transposition.inverse_transpose(unshifted, trans_key, rounds)

        return plaintext

    def _apply_sdes(self, binary: str, key: str, encrypt: bool) -> str:
        """
        Apply the S-DES algorithm to the binary data.

        Args:
            binary:     The binary data to be processed.
            key:        The S-DES key.
            encrypt:    If True, perform encryption; otherwise, perform decryption.

        Returns:
            The processed binary data.
        """
        result = ""
        total_blocks = len(binary) // 8
        operation = "Encrypting" if encrypt else "Decrypting"

        if self.progress_level == ProgressLevel.DETAILED:
            print(f"\n{operation} with S-DES:")
            print(f"Total blocks to process: {total_blocks}")
            print(f"Key: {key}")

        for i in range(0, len(binary), 8):
            block = binary[i:i + 8]
            block_number = i // 8 + 1

            if self.progress_level == ProgressLevel.DETAILED:
                print(f"\n{operation} block {block_number}/{total_blocks}")
                print(f"Input block: {block}")

            if encrypt:
                processed_block = self.sdes.encrypt(block, key)
            else:
                processed_block = self.sdes.decrypt(block, key)

            result += processed_block

            if self.progress_level == ProgressLevel.DETAILED:
                print(f"Output block: {processed_block}")
                print(f"Current result: {result}")

        if self.progress_level == ProgressLevel.DETAILED:
            print(f"\nFinal {operation.lower()[:-3]}ed result: {result}")

        return result

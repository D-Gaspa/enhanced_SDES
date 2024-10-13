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
from utils.utilities import Utilities


class EnhancedSDES:
    """
    A class implementing the Enhanced Simplified Data Encryption Standard.

    This class combines the S-DES algorithm with columnar transposition and
    shift rows operations to provide a more secure encryption scheme.

    Attributes:
        show_progress:  A boolean indicating whether to show intermediate steps.
        transposition:  An instance of ColumnTransposition.
        shift_rows:     An instance of ShiftRows.
        sdes:           An instance of SDES.
        key_manager:    An instance of KeyManager.
    """

    def __init__(self, show_progress: bool = False):
        """
        Initialize the EnhancedSDES instance.

        Args:
            show_progress: If True, intermediate steps will be printed.
        """
        self.show_progress = show_progress
        self.transposition = ColumnTransposition()
        self.shift_rows = ShiftRows()
        self.sdes = SDES()
        self.key_manager = KeyManager()

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
        # Step 1: Columnar Transposition
        transposed = self.transposition.transpose(plaintext, trans_key, rounds)
        if self.show_progress:
            print(f"Columnar Transposition: {transposed}")

        # Step 2: Shift Rows
        shifted = self.shift_rows.shift(transposed, len(trans_key))
        if self.show_progress:
            print(f"Shift Rows: {shifted}")

        # Step 3: S-DES Encryption
        binary = Utilities.text_to_binary(shifted)
        encrypted_binary = self._apply_sdes(binary, sdes_key, encrypt=True)

        cipher_text = Utilities.binary_to_hex(encrypted_binary)
        if self.show_progress:
            print(f"S-DES Encryption: {cipher_text}")

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
        # Step 1: S-DES Decryption
        binary = Utilities.hex_to_binary(ciphertext)
        decrypted_binary = self._apply_sdes(binary, sdes_key, encrypt=False)
        text = Utilities.binary_to_text(decrypted_binary)
        if self.show_progress:
            print(f"S-DES Decryption: {text}")

        # Step 2: Inverse Shift Rows
        unshifted = self.shift_rows.inverse_shift(text, len(trans_key))
        if self.show_progress:
            print(f"Inverse Shift Rows: {unshifted}")

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
        for i in range(0, len(binary), 8):
            block = binary[i:i + 8]
            if encrypt:
                result += self.sdes.encrypt(block, key)
            else:
                result += self.sdes.decrypt(block, key)
        return result

"""
This module provides key management functionality for the enhanced_SDES project.

It includes a class for generating and managing keys for both the S-DES algorithm
and the columnar transposition technique used in the enhanced version.
"""

import random
from typing import List


class KeyManager:
    """
    A class for managing encryption keys.

    This class provides methods for generating keys for the S-DES algorithm
    and the columnar transposition technique used in the enhanced version.
    """
    MIN_COLUMNS = 2
    MAX_COLUMNS = 26  # Maximum number of columns (alphabet size)
    DEFAULT_COLUMNS = 3

    @staticmethod
    def generate_sdes_key() -> str:
        """
        Generate a 10-bit key for S-DES.

        Returns:
            A 10-bit binary string representing the S-DES key.
        """
        return ''.join(random.choice('01') for _ in range(10))

    @staticmethod
    def generate_transposition_key(columns: int = DEFAULT_COLUMNS) -> List[int]:
        """
        Generate a key for columnar transposition.

        Args:
            columns: The number of columns in the transposition matrix.

        Returns:
            A list of integers representing the column order for transposition.
        """
        if columns < KeyManager.MIN_COLUMNS or columns > KeyManager.MAX_COLUMNS:
            raise ValueError(f"Number of columns must be between {KeyManager.MIN_COLUMNS} and {KeyManager.MAX_COLUMNS}")

        key = list(range(1, columns + 1))  # Generate key in base 1
        random.shuffle(key)
        return key

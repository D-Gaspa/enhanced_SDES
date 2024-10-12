"""
This module implements the Columnar Transposition cipher.

It provides a class that encapsulates the encryption and decryption processes
of the Columnar Transposition technique, which is used as part of the enhanced S-DES algorithm.
"""

from math import ceil
from typing import List


class ColumnTransposition:
    """
    A class implementing the Columnar Transposition cipher.

    This class provides methods for encrypting and decrypting text using
    the Columnar Transposition technique.
    It supports multiple rounds of transposition for increased security.
    """

    def transpose(self, text: str, key: List[int], rounds: int = 1) -> str:
        """
        Perform columnar transposition encryption on the input text.

        Args:
            text:   The text to be encrypted.
            key:    A list of integers representing the column order.
            rounds: The number of rounds of transposition to perform.

        Returns:
            The encrypted text after columnar transposition.
        """
        for _ in range(rounds):
            text = self._single_round_transpose(text, key)
        return text

    def inverse_transpose(self, text: str, key: List[int], rounds: int = 1) -> str:
        """
        Perform columnar transposition decryption on the input text.

        Args:
            text:   The text to be decrypted.
            key:    A list of integers representing the column order.
            rounds: The number of rounds of transposition to reverse.

        Returns:
            The decrypted text after reversing columnar transposition.
        """
        inverse_key = self._get_inverse_key(key)
        for _ in range(rounds):
            text = self._single_round_transpose(text, inverse_key)
        return text

    @staticmethod
    def _single_round_transpose(text: str, key: List[int]) -> str:
        """
        Perform a single round of columnar transposition.

        Args:
            text: The text to be transposed.
            key: A list of integers representing the column order.

        Returns:
            The transposed text.
        """
        num_columns = len(key)
        num_rows = ceil(len(text) / num_columns)
        padding = num_columns * num_rows - len(text)

        # Pad the text if necessary
        text += ' ' * padding

        # Create the transposition grid
        grid = [text[i:i + num_columns] for i in range(0, len(text), num_columns)]

        # Read off the columns according to the key
        transposed = ''
        for col in key:
            transposed += ''.join(row[col] for row in grid)

        return transposed.rstrip()

    @staticmethod
    def _get_inverse_key(key: List[int]) -> List[int]:
        """
        Generate the inverse key for decryption.

        Args:
            key: A list of integers representing the column order.

        Returns:
            A list of integers representing the inverse column order.
        """
        inverse = [0] * len(key)
        for i, k in enumerate(key):
            inverse[k] = i
        return inverse

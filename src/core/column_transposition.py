"""
This module implements the Columnar Transposition cipher.

It provides a class that encapsulates the encryption and decryption processes
of the Columnar Transposition technique, which is used as part of the enhanced S-DES algorithm.
"""
import math
from typing import List

from utils.progress_level import ProgressLevel
from utils.utilities import Utilities


class ColumnTransposition:
    """
    A class implementing the Columnar Transposition cipher.

    This class provides methods for encrypting and decrypting text using
    the Columnar Transposition technique.
    It supports multiple rounds of transposition for increased security.

    Attributes:
        progress_level: The level of detail to show during the transposition process.
    """
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self):
        """
        Initialize the ColumnTransposition instance.
        """
        self.progress_level = ProgressLevel.NONE

    def set_progress_level(self, level: ProgressLevel) -> None:
        """
        Set the progress level for the Columnar Transposition cipher.

        Args:
            level: The progress level to set.
        """
        self.progress_level = level

    def transpose(self, text: str, key: List[int], rounds: int = 1) -> str:
        """
        Perform columnar transposition encryption on the input text.

        Args:
            text:           The text to be encrypted.
            key:            A list of integers representing the column order.
            rounds:         The number of rounds of transposition to perform.

        Returns:
            The encrypted text after columnar transposition.
        """
        num_columns = len(key)
        text = self._prepare_text(text, len(key))

        if self.progress_level == ProgressLevel.DETAILED:
            print("Initial Table:")
            print(Utilities.create_table(text, num_columns))

        for round_num in range(rounds):
            text = self._single_round_transpose(text, key)
            if self.progress_level == ProgressLevel.DETAILED:
                print(f"After round {round_num + 1}:")
                print(Utilities.create_table(text, num_columns))

        return text

    def inverse_transpose(self, text: str, key: List[int], rounds: int = 1) -> str:
        """
        Perform columnar transposition decryption on the input text.

        Args:
            text:           The text to be decrypted.
            key:            A list of integers representing the column order.
            rounds:         The number of rounds of transposition to reverse.

        Returns:
            The decrypted text after reversing columnar transposition.
        """
        inverse_key = self._get_inverse_key(key)
        num_columns = len(key)

        if self.progress_level == ProgressLevel.DETAILED:
            print("Initial Table:")
            print(Utilities.create_table(text, num_columns))

        for round_num in range(rounds):
            text = self._single_round_inverse_transpose(text, inverse_key)
            if self.progress_level == ProgressLevel.DETAILED:
                print(f"After round {round_num + 1}:")
                print(Utilities.create_table(text, num_columns))

        return text.strip()

    @staticmethod
    def _prepare_text(text: str, num_columns: int) -> str:
        """
        Prepare the text for transposition by removing spaces and adding padding.

        Args:
            text:        The input text to be prepared.
            num_columns: The number of columns in the transposition.

        Returns:
            The prepared text with spaces removed and padding added.
        """
        padding_length = -len(text) % num_columns
        if padding_length > 0:
            padding = ' ' * padding_length
            text += padding
        return text

    @staticmethod
    def _single_round_transpose(text: str, key: List[int]) -> str:
        """
        Perform a single round of columnar transposition.

        Args:
            text:   The text to be transposed.
            key:    A list of integers representing the column order.

        Returns:
            The transposed text.
        """
        num_columns = len(key)
        grid = [''] * num_columns

        for i, char in enumerate(text):
            grid[key[i % num_columns] - 1] += char

        return ''.join(grid)

    @staticmethod
    def _single_round_inverse_transpose(text: str, key: List[int]) -> str:
        """
        Perform a single round of inverse columnar transposition

        Args:
            text:   The text to be transposed.
            key:    A list of integers representing the column order.

        Returns:
            The transposed text.
        """
        num_columns = len(key)
        num_rows = math.ceil(len(text) / num_columns)
        column_lengths = [num_rows] * num_columns

        for i in range(len(text) % num_columns):
            column_lengths[key[i] - 1] -= 1

        columns = [''] * num_columns
        index = 0
        for i, length in enumerate(column_lengths):
            columns[key[i] - 1] = text[index:index + length]
            index += length

        result = ''
        for i in range(max(column_lengths)):
            for col in columns:
                if i < len(col):
                    result += col[i]

        return result

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
        for i, k in enumerate(key, 1):
            inverse[k - 1] = i
        return inverse

"""
This module implements the Shift Rows operation for the enhanced S-DES algorithm.

It provides a class that encapsulates the shift and inverse shift operations
used in the enhanced version of the Simplified Data Encryption Standard (S-DES).
"""

from math import ceil

from utils.progress_level import ProgressLevel
from utils.utilities import Utilities


class ShiftRows:
    """
    A class implementing the Shift Rows operation.

    This class provides methods for shifting rows of a matrix of characters,
    as well as the inverse operation.
    It is used as part of the enhanced S-DES algorithm and can handle matrices of various sizes.

    Attributes:
        progress_level: The level of detail to show during the shift operation.
    """

    def __init__(self):
        """
        Initialize the ShiftRows instance.
        """
        self.progress_level = ProgressLevel.NONE

    def set_progress_level(self, level: ProgressLevel) -> None:
        """
        Set the progress level for the Shift Rows operation.

        Args:
            level: The progress level to set.
        """
        self.progress_level = level

    def shift(self, text: str, num_columns: int) -> str:
        """
        Perform the Shift Rows operation on the input text.

        The operation shifts rows as follows:
        - First row: no shift
        - Second row: shift one position to the left
        - Third row: shift two positions to the left
        - And so on for any additional rows

        Args:
            text:           A string of characters to be arranged in a matrix and shifted.
            num_columns:    The number of columns in the matrix.

        Returns:
            A string of characters after the shift operation.
        """
        num_rows = ceil(len(text) / num_columns)
        matrix = [list(text[i:i + num_columns].ljust(num_columns)) for i in range(0, len(text), num_columns)]

        if self.progress_level == ProgressLevel.DETAILED:
            print("Before Shift:")
            print(Utilities.create_table(''.join(''.join(row).rstrip() for row in matrix), num_columns))

        for i in range(1, num_rows):
            matrix[i] = matrix[i][i:] + matrix[i][:i]

        result = ''.join(''.join(row).rstrip() for row in matrix)

        if self.progress_level == ProgressLevel.DETAILED:
            print("After Shift:")
            print(Utilities.create_table(result, num_columns))

        return result

    def inverse_shift(self, text: str, num_columns: int) -> str:
        """
        Perform the inverse Shift Rows operation on the input text.

        The operation shifts rows as follows:
        - First row: no shift
        - Second row: shift one position to the right
        - Third row: shift two positions to the right
        - And so on for any additional rows

        Args:
            text:           A string of characters to be arranged in a matrix and inverse shifted.
            num_columns:    The number of columns in the matrix.

        Returns:
            A string of characters after the inverse shift operation.
        """
        num_rows = ceil(len(text) / num_columns)
        matrix = [list(text[i:i + num_columns].ljust(num_columns)) for i in range(0, len(text), num_columns)]

        if self.progress_level == ProgressLevel.DETAILED:
            print("Before Inverse Shift:")
            print(Utilities.create_table(''.join(''.join(row).rstrip() for row in matrix), num_columns))

        for i in range(1, num_rows):
            matrix[i] = matrix[i][-i:] + matrix[i][:-i]

        result = ''.join(''.join(row).rstrip() for row in matrix)

        if self.progress_level == ProgressLevel.DETAILED:
            print("After Inverse Shift:")
            print(Utilities.create_table(result, num_columns))

        return result

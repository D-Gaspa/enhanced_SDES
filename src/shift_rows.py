"""
This module implements the Shift Rows operation for the enhanced S-DES algorithm.

It provides a class that encapsulates the shift and inverse shift operations
used in the enhanced version of the Simplified Data Encryption Standard (S-DES).
"""


class ShiftRows:
    """
    A class implementing the Shift Rows operation.

    This class provides methods for shifting rows of a 3x3 matrix of characters,
    as well as the inverse operation.
    It is used as part of the enhanced S-DES algorithm.
    """

    @staticmethod
    def shift(text: str) -> str:
        """
        Perform the Shift Rows operation on the input text.

        The operation shifts the rows of a 3x3 matrix as follows:
        - First row: no shift
        - Second row: shift one position to the left
        - Third row: shift two positions to the left

        Args:
            text: A string of nine characters to be arranged in a 3x3 matrix and shifted.

        Returns:
            A string of nine characters after the shift operation.

        Raises:
            ValueError: If the input text is not exactly nine characters long.
        """
        if len(text) != 9:
            raise ValueError("Input text must be exactly 9 characters long")

        matrix = [list(text[i:i + 3]) for i in range(0, 9, 3)]

        # Shift second row
        matrix[1] = matrix[1][1:] + [matrix[1][0]]

        # Shift third row
        matrix[2] = matrix[2][2:] + matrix[2][:2]

        return ''.join(''.join(row) for row in matrix)

    @staticmethod
    def inverse_shift(text: str) -> str:
        """
        Perform the inverse Shift Rows operation on the input text.

        The operation shifts the rows of a 3x3 matrix as follows:
        - First row: no shift
        - Second row: shift one position to the right
        - Third row: shift two positions to the right

        Args:
            text: A string of nine characters to be arranged in a 3x3 matrix and inverse shifted.

        Returns:
            A string of nine characters after the inverse shift operation.

        Raises:
            ValueError: If the input text is not exactly nine characters long.
        """
        if len(text) != 9:
            raise ValueError("Input text must be exactly 9 characters long")

        matrix = [list(text[i:i + 3]) for i in range(0, 9, 3)]

        # Inverse shift second row
        matrix[1] = [matrix[1][-1]] + matrix[1][:-1]

        # Inverse shift third row
        matrix[2] = matrix[2][-2:] + matrix[2][:-2]

        return ''.join(''.join(row) for row in matrix)

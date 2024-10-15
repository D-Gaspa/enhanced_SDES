"""
This module provides utility functions and classes for the enhanced_SDES project.

It includes functions for text-to-binary conversion, binary-to-text conversion,
splitting data into blocks, and a decorator for showing progress of operations.
"""
import math

from tabulate import tabulate


class Utilities:
    """
    A utility class providing static methods for various data manipulations.

    This class contains methods for converting between text and binary representations,
    between binary and hexadecimal representations, and for creating tabular
    representations of data.
    """

    @staticmethod
    def text_to_binary(text: str) -> str:
        """
        Convert a string of text to its binary representation.

        Args:
            text: The input text to be converted.

        Returns:
            The binary representation of the input text.
        """
        return ''.join(format(ord(char), '08b') for char in text)

    @staticmethod
    def binary_to_text(binary: str) -> str:
        """
        Convert a binary string to its text representation.

        Args:
            binary: The binary string to be converted.

        Returns:
            The text representation of the input binary string.
        """
        return ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))

    @staticmethod
    def binary_to_hex(binary: str) -> str:
        """
        Convert a binary string to its hexadecimal representation.

        Args:
            binary: The binary string to be converted.

        Returns:
            The hexadecimal representation of the input binary string.
        """
        return hex(int(binary, 2))[2:].upper().zfill(len(binary) // 4)

    @staticmethod
    def hex_to_binary(hex_string: str) -> str:
        """
        Convert a hexadecimal string to its binary representation.

        Args:
            hex_string: The hexadecimal string to be converted.

        Returns:
            The binary representation of the input hexadecimal string.
        """
        return bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)

    @staticmethod
    def create_table(text: str, num_columns: int) -> str:
        """
        Create a tabular representation of the text.

        Args:
            text:           The text to be represented in a table.
            num_columns:    The number of columns in the table.

        Returns:
            A string representation of the table.
        """

        num_rows = math.ceil(len(text) / num_columns)
        table = []

        for i in range(num_rows):
            row = list(text[i * num_columns: (i + 1) * num_columns])
            row += [''] * (num_columns - len(row))  # Pad with empty strings if necessary
            table.append(row)

        headers = [f"Col {i + 1}" for i in range(num_columns)]
        return tabulate(table, headers=headers, tablefmt="grid")

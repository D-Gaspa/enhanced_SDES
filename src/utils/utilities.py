"""
This module provides utility functions and classes for the enhanced_SDES project.

It includes functions for text-to-binary conversion, binary-to-text conversion,
splitting data into blocks, and a decorator for showing progress of operations.
"""


class Utilities:
    """
    A utility class providing static methods for various data manipulations.

    This class contains methods for converting between a text and binary representations,
    as well as between binary and hexadecimal representations.
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


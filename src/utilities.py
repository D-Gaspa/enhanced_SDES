"""
This module provides utility functions and classes for the enhanced_SDES project.

It includes functions for text-to-binary conversion, binary-to-text conversion,
splitting data into blocks, and a decorator for showing progress of operations.
"""

from typing import Callable, Any


class Utilities:
    """
    A utility class providing static methods for various data manipulations.

    This class contains methods for converting between a text and binary representations,
    splitting data into blocks, and other utility functions used throughout the project.
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


def show_progress(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator to optionally show the progress of a function.

    This decorator will print the function name and its result if the
    'show_progress' attribute of the class instance is True.

    Args:
        func: The function to be decorated.

    Returns:
        The wrapped function.
    """

    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Wrapper function that adds progress reporting to the decorated function.

        Args:
            self:       The instance of the class (if it's a method).
            *args:      Positional arguments passed to the decorated function.
            **kwargs:   Keyword arguments passed to the decorated function.

        Returns:
            The result of the decorated function.
        """
        result = func(self, *args, **kwargs)
        if self.show_progress:
            print(f"{func.__name__}: {result}")
        return result

    return wrapper

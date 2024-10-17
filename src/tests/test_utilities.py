"""
This module contains unit tests for the utilities module.

It includes test cases for various utility functions such as
text-to-binary conversion, binary-to-text conversion, and other
helper functions used in the Enhanced S-DES project.
"""

import unittest

from src.utils.utilities import Utilities


class TestUtilities(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by initializing the Utilities class.
        """
        self.utilities = Utilities()

    def test_text_to_binary(self):
        self.assertEqual(self.utilities.text_to_binary("A"), "01000001")
        self.assertEqual(self.utilities.text_to_binary("AB"), "0100000101000010")
        self.assertEqual(self.utilities.text_to_binary("Hello"), "0100100001100101011011000110110001101111")

    def test_binary_to_text(self):
        self.assertEqual(self.utilities.binary_to_text("01000001"), "A")
        self.assertEqual(self.utilities.binary_to_text("0100000101000010"), "AB")
        self.assertEqual(self.utilities.binary_to_text("0100100001100101011011000110110001101111"), "Hello")

    def test_binary_to_hex(self):
        self.assertEqual(self.utilities.binary_to_hex("01000001"), "41")
        self.assertEqual(self.utilities.binary_to_hex("0100000101000010"), "4142")
        self.assertEqual(self.utilities.binary_to_hex("0100100001100101011011000110110001101111"), "48656C6C6F")

    def test_hex_to_binary(self):
        self.assertEqual(self.utilities.hex_to_binary("41"), "01000001")
        self.assertEqual(self.utilities.hex_to_binary("4142"), "0100000101000010")
        self.assertEqual(self.utilities.hex_to_binary("48656C6C6F"), "0100100001100101011011000110110001101111")

    def test_text_to_binary_and_back(self):
        original_text = "Hello, World!"
        binary = self.utilities.text_to_binary(original_text)
        decoded_text = self.utilities.binary_to_text(binary)
        self.assertEqual(original_text, decoded_text)


if __name__ == '__main__':
    unittest.main()

"""
This module contains unit tests for the shift_rows module.

It includes test cases for the shift and inverse shift operations
used in the enhanced version of the Simplified Data Encryption Standard (S-DES).
"""

import unittest

from src.core.shift_rows import ShiftRows


class TestShiftRows(unittest.TestCase):
    def setUp(self):
        """
        Initialize the ShiftRows instance for testing.
        """
        self.sr = ShiftRows()

    def test_shift_3x3(self):
        text = "ABCDEFGHI"
        num_columns = 3
        expected = "ABCEFDIGH"
        result = self.sr.shift(text, num_columns)
        self.assertEqual(result, expected)

    def test_inverse_shift_3x3(self):
        text = "ABCEFDIGH"
        num_columns = 3
        expected = "ABCDEFGHI"
        result = self.sr.inverse_shift(text, num_columns)
        self.assertEqual(result, expected)

    def test_shift_4x4(self):
        text = "ABCDEFGHIJKLMNOP"
        num_columns = 4
        expected = "ABCDFGHEKLIJPMNO"
        result = self.sr.shift(text, num_columns)
        self.assertEqual(result, expected)

    def test_inverse_shift_4x4(self):
        text = "ABCDFGHEKLIJPMNO"
        num_columns = 4
        expected = "ABCDEFGHIJKLMNOP"
        result = self.sr.inverse_shift(text, num_columns)
        self.assertEqual(result, expected)

    def test_shift_non_square(self):
        text = "ABCDEFGHIJKL"
        num_columns = 4
        expected = "ABCDFGHEKLIJ"
        result = self.sr.shift(text, num_columns)
        self.assertEqual(result, expected)

    def test_inverse_shift_non_square(self):
        text = "ABCDFGHEKLIJ"
        num_columns = 4
        expected = "ABCDEFGHIJKL"
        result = self.sr.inverse_shift(text, num_columns)
        self.assertEqual(result, expected)

    def test_shift_long_text(self):
        text = "ATTACKPOSTPONEDUNTILTWOAMXYZ"
        num_columns = 7
        expected = "ATTACKPSTPONEONTILTDUMXYZWOA"
        result = self.sr.shift(text, num_columns)
        self.assertEqual(result, expected)

    def test_inverse_shift_long_text(self):
        text = "ATTACKPSTPONEONTILTDUMXYZWOA"
        num_columns = 7
        expected = "ATTACKPOSTPONEDUNTILTWOAMXYZ"
        result = self.sr.inverse_shift(text, num_columns)
        self.assertEqual(result, expected)

    def test_shift_then_inverse(self):
        original = "ABCDEFGHI"
        num_columns = 3
        shifted = self.sr.shift(original, num_columns)
        result = self.sr.inverse_shift(shifted, num_columns)
        self.assertEqual(result, original)


if __name__ == '__main__':
    unittest.main()

"""
This module contains unit tests for the column_transposition module.

It includes test cases for encryption and decryption using the
Columnar Transposition cipher, as well as edge cases and error handling.
"""

import unittest

from src.core.column_transposition import ColumnTransposition


class TestColumnTransposition(unittest.TestCase):
    def setUp(self):
        """
        Initialize the ColumnTransposition instance for testing.
        """
        self.ct = ColumnTransposition()

    def test_single_round_transpose_short(self):
        text = "DID YOU SEE"
        key = [3, 1, 2]
        expected = "IOEDUEDYS"
        result = self.ct.transpose(text, key)
        self.assertEqual(result, expected)

    def test_double_round_transpose_short(self):
        text = "DID YOU SEE"
        key = [3, 1, 2]
        expected_first_round = "IOEDUEDYS"
        expected_second_round = "OUYEESIDD"
        first_round = self.ct.transpose(text, key)
        self.assertEqual(first_round, expected_first_round)
        second_round = self.ct.transpose(first_round, key)
        self.assertEqual(second_round, expected_second_round)

    def test_inverse_transpose_short(self):
        ciphertext = "IOEDUEDYS"
        key = [3, 1, 2]
        expected = "DIDYOUSEE"
        result = self.ct.inverse_transpose(ciphertext, key)
        self.assertEqual(result, expected)

    def test_double_inverse_transpose_short(self):
        ciphertext = "OUYEESIDD"
        key = [3, 1, 2]
        expected = "DIDYOUSEE"
        result = self.ct.inverse_transpose(ciphertext, key, rounds=2)
        self.assertEqual(result, expected)

    def test_single_round_transpose_long(self):
        text = "ATTACKPOSTPONEDUNTILTWOAM"
        key = [4, 3, 1, 2, 5, 6, 7]
        expected = "TTNAAPTMTSUOAODWCOIXKNLYPETZ"
        result = self.ct.transpose(text, key)
        self.assertEqual(result, expected)

    def test_double_round_transpose_long(self):
        text = "ATTACKPOSTPONEDUNTILTWOAM"
        key = [4, 3, 1, 2, 5, 6, 7]
        expected_first_round = "TTNAAPTMTSUOAODWCOIXKNLYPETZ"
        expected_second_round = "NSCYAUOPTTWLTMDNAOIEPAXTTOKZ"
        first_round = self.ct.transpose(text, key)
        self.assertEqual(first_round, expected_first_round)
        second_round = self.ct.transpose(first_round, key)
        self.assertEqual(second_round, expected_second_round)

    def test_inverse_transpose_long(self):
        ciphertext = "TTNAAPTMTSUOAODWCOIXKNLYPETZ"
        key = [4, 3, 1, 2, 5, 6, 7]
        expected = "ATTACKPOSTPONEDUNTILTWOAMXYZ"
        result = self.ct.inverse_transpose(ciphertext, key)
        self.assertEqual(result, expected)

    def test_double_inverse_transpose_long(self):
        ciphertext = "NSCYAUOPTTWLTMDNAOIEPAXTTOKZ"
        key = [4, 3, 1, 2, 5, 6, 7]
        expected = "ATTACKPOSTPONEDUNTILTWOAMXYZ"
        result = self.ct.inverse_transpose(ciphertext, key, rounds=2)
        self.assertEqual(result, expected)

    def test_transpose_and_inverse(self):
        text = "WEWEREDISCOVEREDYESTERDAY"
        key = [3, 1, 4, 2, 5]
        encrypted = self.ct.transpose(text, key)
        decrypted = self.ct.inverse_transpose(encrypted, key)
        self.assertEqual(text, decrypted)

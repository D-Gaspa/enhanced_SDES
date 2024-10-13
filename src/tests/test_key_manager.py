"""
This module contains unit tests for the key_manager module.

It includes test cases for generating S-DES keys and transposition keys,
as well as error handling for invalid inputs.
"""

import unittest

from src.utils.key_manager import KeyManager


class TestKeyManager(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case with a KeyManager instance.
        """
        self.key_manager = KeyManager()

    def test_generate_sdes_key(self):
        key = self.key_manager.generate_sdes_key()
        self.assertEqual(len(key), 10)
        self.assertTrue(all(bit in '01' for bit in key))

    def test_generate_multiple_transposition_keys(self):
        columns = 5
        keys = [self.key_manager.generate_transposition_key(columns) for _ in range(100)]
        self.assertTrue(any(keys[i] != keys[j] for i in range(len(keys)) for j in range(i + 1, len(keys))))

    def test_generate_transposition_key(self):
        columns = 5
        key = self.key_manager.generate_transposition_key(columns)
        self.assertEqual(len(key), columns)
        self.assertEqual(set(key), set(range(1, columns + 1)))

    def test_generate_transposition_key_constraints(self):
        with self.assertRaises(ValueError):
            self.key_manager.generate_transposition_key(1)
        with self.assertRaises(ValueError):
            self.key_manager.generate_transposition_key(27)

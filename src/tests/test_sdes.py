"""
This module contains unit tests for the sdes module.

It includes test cases for key generation, encryption, decryption,
and various components of the Simplified Data Encryption Standard (S-DES) algorithm.
"""
import random
import unittest

from src.core.sdes import SDES
from src.utils.key_manager import KeyManager
from src.utils.utilities import Utilities


class TestSDES(unittest.TestCase):
    def setUp(self):
        """
        Initialize the SDES instance for testing.
        """
        self.sdes = SDES()

    def test_encrypt_decrypt(self):
        plaintext = "10101010"
        key = "1010101010"
        ciphertext = self.sdes.encrypt(plaintext, key)
        decrypted = self.sdes.decrypt(ciphertext, key)
        self.assertEqual(plaintext, decrypted)

    def test_generate_subkeys(self):
        key = "1010101010"
        subkey1, subkey2 = self.sdes.generate_subkeys(key)
        self.assertEqual(len(subkey1), 8)
        self.assertEqual(len(subkey2), 8)
        self.assertNotEqual(subkey1, subkey2)

    def test_permute(self):
        bits = "10101010"
        table = [2, 4, 6, 8, 1, 3, 5, 7]
        expected = "00001111"
        result = self.sdes._permute(bits, table)
        self.assertEqual(result, expected)

    def test_sbox(self):
        bits = "1010"
        sbox = self.sdes.S0
        result = self.sdes._sbox(bits, sbox)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(bit in '01' for bit in result))

    def test_xor(self):
        bits1 = "1010"
        bits2 = "1100"
        expected = "0110"
        result = self.sdes._xor(bits1, bits2)
        self.assertEqual(result, expected)

    def test_left_shift(self):
        bits = "11001"
        shifted = self.sdes._left_shift(bits, 2)
        self.assertEqual(shifted, "00111")

    def test_round_function(self):
        input_bits = "10101010"
        subkey = "10101010"
        result = self.sdes._round_function(input_bits, subkey)
        self.assertEqual(len(result), 8)
        self.assertTrue(all(bit in '01' for bit in result))

    def test_multiple_encrypt_decrypt(self):
        for _ in range(100):
            plaintext = ''.join(Utilities.text_to_binary(chr(random.randint(0, 255))))
            key = KeyManager.generate_sdes_key()
            ciphertext = self.sdes.encrypt(plaintext, key)
            decrypted = self.sdes.decrypt(ciphertext, key)
            self.assertEqual(plaintext, decrypted)


if __name__ == '__main__':
    unittest.main()

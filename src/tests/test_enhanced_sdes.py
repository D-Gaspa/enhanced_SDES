"""
This module contains unit tests for the enhanced_sdes module.

It includes test cases for encryption, decryption, and the overall
functionality of the Enhanced Simplified Data Encryption Standard (Enhanced S-DES).
"""

import unittest

from core.enhanced_sdes import EnhancedSDES
from utils.key_manager import KeyManager


class TestEnhancedSDES(unittest.TestCase):
    def setUp(self):
        """
        Initialize the EnhancedSDES instance for testing.
        """
        self.esdes = EnhancedSDES()
        self.key_manager = KeyManager()

    def test_encrypt_decrypt_short_message(self):
        plaintext = "HELLOZ"
        sdes_key = self.key_manager.generate_sdes_key()
        trans_key = self.key_manager.generate_transposition_key(3)
        rounds = 2

        ciphertext = self.esdes.encrypt(plaintext, sdes_key, trans_key, rounds)
        decrypted = self.esdes.decrypt(ciphertext, sdes_key, trans_key, rounds)

        self.assertEqual(plaintext, decrypted)

    def test_encrypt_decrypt_long_message(self):
        plaintext = "ATTACKPOSTPONEDUNTILTWOAM"
        sdes_key = self.key_manager.generate_sdes_key()
        trans_key = self.key_manager.generate_transposition_key(5)
        rounds = 3

        ciphertext = self.esdes.encrypt(plaintext, sdes_key, trans_key, rounds)
        decrypted = self.esdes.decrypt(ciphertext, sdes_key, trans_key, rounds)

        self.assertEqual(plaintext, decrypted)

    def test_encrypt_decrypt_with_spaces(self):
        plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
        sdes_key = self.key_manager.generate_sdes_key()
        trans_key = self.key_manager.generate_transposition_key(7)
        rounds = 2

        ciphertext = self.esdes.encrypt(plaintext, sdes_key, trans_key, rounds)
        decrypted = self.esdes.decrypt(ciphertext, sdes_key, trans_key, rounds)

        self.assertEqual(plaintext, decrypted)

    def test_encrypt_decrypt_multiple_rounds(self):
        plaintext = "CONFIDENTIALMESSAGEZ"
        sdes_key = self.key_manager.generate_sdes_key()
        trans_key = self.key_manager.generate_transposition_key(4)

        for rounds in range(1, 6):
            ciphertext = self.esdes.encrypt(plaintext, sdes_key, trans_key, rounds)
            decrypted = self.esdes.decrypt(ciphertext, sdes_key, trans_key, rounds)
            self.assertEqual(plaintext, decrypted)

    def test_different_keys_produce_different_ciphertexts(self):
        plaintext = "SECRETMESSAGE"
        sdes_key1 = self.key_manager.generate_sdes_key()
        sdes_key2 = self.key_manager.generate_sdes_key()
        trans_key1 = self.key_manager.generate_transposition_key(4)
        trans_key2 = self.key_manager.generate_transposition_key(4)
        rounds = 2

        ciphertext1 = self.esdes.encrypt(plaintext, sdes_key1, trans_key1, rounds)
        ciphertext2 = self.esdes.encrypt(plaintext, sdes_key2, trans_key2, rounds)

        self.assertNotEqual(ciphertext1, ciphertext2)

    def test_wrong_key_fails_decryption(self):
        plaintext = "TOPSECRET"
        correct_sdes_key = self.key_manager.generate_sdes_key()
        wrong_sdes_key = self.key_manager.generate_sdes_key()
        correct_trans_key = self.key_manager.generate_transposition_key(3)
        wrong_trans_key = self.key_manager.generate_transposition_key(3)
        rounds = 2

        ciphertext = self.esdes.encrypt(plaintext, correct_sdes_key, correct_trans_key, rounds)

        wrong_plaintext = self.esdes.decrypt(ciphertext, wrong_sdes_key, correct_trans_key, rounds)
        self.assertNotEqual(plaintext, wrong_plaintext)

        wrong_plaintext = self.esdes.decrypt(ciphertext, correct_sdes_key, wrong_trans_key, rounds)
        self.assertNotEqual(plaintext, wrong_plaintext)

    def test_encryption_changes_plaintext(self):
        plaintext = "PLAINTEXT"
        sdes_key = self.key_manager.generate_sdes_key()
        trans_key = self.key_manager.generate_transposition_key(3)
        rounds = 2

        ciphertext = self.esdes.encrypt(plaintext, sdes_key, trans_key, rounds)
        self.assertNotEqual(plaintext, ciphertext)

    def test_multiple_encryptions_produce_same_result(self):
        plaintext = "CONSISTENCY"
        sdes_key = self.key_manager.generate_sdes_key()
        trans_key = self.key_manager.generate_transposition_key(5)
        rounds = 2

        ciphertext1 = self.esdes.encrypt(plaintext, sdes_key, trans_key, rounds)
        ciphertext2 = self.esdes.encrypt(plaintext, sdes_key, trans_key, rounds)
        self.assertEqual(ciphertext1, ciphertext2)

    def test_correct_hex_output(self):
        plaintext = "DIDYOUSEE"
        sdes_key = "0010010111"
        rounds = 2

        expected_ciphertext = "CF4A218C4C8C7C827C"
        ciphertext = self.esdes.encrypt(plaintext, sdes_key, [3, 1, 2], rounds)
        self.assertEqual(ciphertext, expected_ciphertext)

    def test_correct_decryption_with_hex_input(self):
        ciphertext = "CF4A218C4C8C7C827C"
        sdes_key = "0010010111"
        rounds = 2

        expected_plaintext = "DIDYOUSEE"
        plaintext = self.esdes.decrypt(ciphertext, sdes_key, [3, 1, 2], rounds)
        self.assertEqual(plaintext, expected_plaintext)


if __name__ == '__main__':
    unittest.main()

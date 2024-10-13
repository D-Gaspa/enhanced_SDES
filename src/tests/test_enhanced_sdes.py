"""
This module contains unit tests for the utilities, key manager, and SDES classes.

It includes test cases for the text-to-binary and binary-to-text conversion functions,
splitting data into blocks, generating SDES keys, and encrypting and decrypting data using SDES.
"""

import random
import unittest

from column_transposition import ColumnTransposition
from enhanced_sdes import EnhancedSDES
from key_manager import KeyManager
from sdes import SDES
from shift_rows import ShiftRows
from utilities import Utilities


class TestUtilities(unittest.TestCase):
    def test_text_to_binary(self):
        self.assertEqual(Utilities.text_to_binary("A"), "01000001")
        self.assertEqual(Utilities.text_to_binary("AB"), "0100000101000010")
        self.assertEqual(Utilities.text_to_binary("Hello"), "0100100001100101011011000110110001101111")

    def test_binary_to_text(self):
        self.assertEqual(Utilities.binary_to_text("01000001"), "A")
        self.assertEqual(Utilities.binary_to_text("0100000101000010"), "AB")
        self.assertEqual(Utilities.binary_to_text("0100100001100101011011000110110001101111"), "Hello")

    def test_binary_to_hex(self):
        self.assertEqual(Utilities.binary_to_hex("01000001"), "41")
        self.assertEqual(Utilities.binary_to_hex("0100000101000010"), "4142")
        self.assertEqual(Utilities.binary_to_hex("0100100001100101011011000110110001101111"), "48656C6C6F")

    def test_hex_to_binary(self):
        self.assertEqual(Utilities.hex_to_binary("41"), "01000001")
        self.assertEqual(Utilities.hex_to_binary("4142"), "0100000101000010")
        self.assertEqual(Utilities.hex_to_binary("48656C6C6F"), "0100100001100101011011000110110001101111")

    def test_text_to_binary_and_back(self):
        original_text = "Hello, World!"
        binary = Utilities.text_to_binary(original_text)
        decoded_text = Utilities.binary_to_text(binary)
        self.assertEqual(original_text, decoded_text)


class TestKeyManager(unittest.TestCase):
    def test_generate_sdes_key(self):
        key = KeyManager.generate_sdes_key()
        self.assertEqual(len(key), 10)
        self.assertTrue(all(bit in '01' for bit in key))

    def test_generate_multiple_transposition_keys(self):
        columns = 5
        keys = [KeyManager.generate_transposition_key(columns) for _ in range(100)]
        self.assertTrue(any(keys[i] != keys[j] for i in range(len(keys)) for j in range(i + 1, len(keys))))

    def test_generate_transposition_key(self):
        columns = 5
        key = KeyManager.generate_transposition_key(columns)
        self.assertEqual(len(key), columns)
        self.assertEqual(set(key), set(range(1, columns + 1)))

    def test_generate_transposition_key_constraints(self):
        with self.assertRaises(ValueError):
            KeyManager.generate_transposition_key(1)
        with self.assertRaises(ValueError):
            KeyManager.generate_transposition_key(27)


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

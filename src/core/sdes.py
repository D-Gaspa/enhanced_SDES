"""
This module implements the Simplified Data Encryption Standard (S-DES) algorithm.

It provides a class that encapsulates the encryption and decryption processes
of the S-DES algorithm, including key generation and various permutation operations.
"""

from typing import List, Tuple


class SDES:
    """
    A class implementing the Simplified Data Encryption Standard (S-DES) algorithm.

    This class provides methods for encryption, decryption, and subkey generation
    using the S-DES algorithm.
    It includes various permutation and substitution operations as defined in the S-DES specification.

    Attributes:
        IP:     Initial Permutation
        IP_INV: Inverse of Initial Permutation
        EP:     Expansion Permutation
        P4:     4-bit Permutation
        P10:    10-bit Permutation
        P8:     8-bit Permutation
        S0:     S-Box 0
        S1:     S-Box 1
    """

    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
    EP = [4, 1, 2, 3, 2, 3, 4, 1]
    P4 = [2, 4, 3, 1]
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]
    S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
    S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Encrypt the given plaintext using S-DES with the provided key.

        Args:
            plaintext:  An 8-bit binary string to be encrypted.
            key:        A 10-bit binary string used as the encryption key.

        Returns:
            An 8-bit binary string representing the encrypted ciphertext.
        """
        return self._crypt(plaintext, key, encrypt=True)

    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Decrypt the given ciphertext using S-DES with the provided key.

        Args:
            ciphertext: An 8-bit binary string to be decrypted.
            key:        A 10-bit binary string used as the decryption key.

        Returns:
            An 8-bit binary string representing the decrypted plaintext.
        """
        return self._crypt(ciphertext, key, encrypt=False)

    def _crypt(self, text: str, key: str, encrypt: bool) -> str:
        """
        Perform encryption or decryption based on the encrypt flag.

        Args:
            text:       An 8-bit binary string to be encrypted or decrypted.
            key:        A 10-bit binary string used as the key.
            encrypt:    Boolean flag to determine encryption (True) or decryption (False).

        Returns:
            An 8-bit binary string representing the result of encryption or decryption.
        """
        subkey1, subkey2 = self.generate_subkeys(key)

        permuted_text = self._permute(text, self.IP)

        # First round
        first_round_key = subkey1 if encrypt else subkey2
        first_round_output = self._round_function(permuted_text, first_round_key)

        switched_halves = self._switch(first_round_output)

        # Second round
        second_round_key = subkey2 if encrypt else subkey1
        second_round_output = self._round_function(switched_halves, second_round_key)

        final_permutation = self._permute(second_round_output, self.IP_INV)
        return final_permutation

    def generate_subkeys(self, key: str) -> Tuple[str, str]:
        """
        Generate two 8-bit subkeys from the 10-bit input key.

        Args:
            key: A 10-bit binary string used as the input key.

        Returns:
            A tuple containing two 8-bit binary strings (K1, K2).
        """
        permuted_10bit_key = self._permute(key, self.P10)

        left_half, right_half = permuted_10bit_key[:5], permuted_10bit_key[5:]

        shifted_for_k1 = self._left_shift(left_half, 1) + self._left_shift(right_half, 1)
        subkey1 = self._permute(shifted_for_k1, self.P8)

        shifted_for_k2 = self._left_shift(left_half, 3) + self._left_shift(right_half, 3)
        subkey2 = self._permute(shifted_for_k2, self.P8)

        return subkey1, subkey2

    def _round_function(self, input_bits: str, subkey: str) -> str:
        """
        Perform one round of the S-DES algorithm (the fK function).

        Args:
            input_bits: An 8-bit binary string.
            subkey:     An 8-bit binary string subkey.

        Returns:
            An 8-bit binary string after applying the round function.
        """
        left_half, right_half = input_bits[:4], input_bits[4:]
        expanded_right_half = self._permute(right_half, self.EP)
        xored_with_key = self._xor(expanded_right_half, subkey)

        s0_output = self._sbox(xored_with_key[:4], self.S0)
        s1_output = self._sbox(xored_with_key[4:], self.S1)
        sbox_combined_output = s0_output + s1_output

        permuted_sbox_output = self._permute(sbox_combined_output, self.P4)
        new_left_half = self._xor(left_half, permuted_sbox_output)
        return new_left_half + right_half

    @staticmethod
    def _permute(bits: str, table: List[int]) -> str:
        """
        Permute the input bits according to the given permutation table.

        Args:
            bits:   A binary string to be permuted.
            table:  A list of indices defining the permutation.

        Returns:
            A binary string after applying the permutation.
        """
        return ''.join(bits[i - 1] for i in table)

    @staticmethod
    def _sbox(bits: str, sbox: List[List[int]]) -> str:
        """
        Apply an S-box substitution.

        Args:
            bits: A 4-bit binary string.
            sbox: A 4x4 S-box table.

        Returns:
            A 2-bit binary string after S-box substitution.
        """
        row = int(bits[0] + bits[3], 2)
        col = int(bits[1:3], 2)
        return format(sbox[row][col], '02b')

    @staticmethod
    def _xor(bits1: str, bits2: str) -> str:
        """
        Perform bitwise XOR on two binary strings.

        Args:
            bits1: First binary string.
            bits2: Second binary string.

        Returns:
            A binary string resulting from bitwise XOR of inputs.
        """
        return ''.join(str(int(a) ^ int(b)) for a, b in zip(bits1, bits2))

    @staticmethod
    def _switch(bits: str) -> str:
        """
        Perform the switch operation by swapping the left and right halves.

        Args:
            bits: An 8-bit binary string.

        Returns:
            An 8-bit binary string with left and right halves swapped.
        """
        return bits[4:] + bits[:4]

    @staticmethod
    def _left_shift(bits: str, n: int) -> str:
        """
        Perform a circular left shift on the input bits.

        Args:
            bits:   A binary string to be shifted.
            n:      Number of positions to shift.

        Returns:
            A binary string after performing the circular left shift.
        """
        return bits[n:] + bits[:n]

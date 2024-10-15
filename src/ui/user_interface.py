"""
This module provides a user interface for the Enhanced S-DES encryption system.

It handles user input, guides the user through the encryption and decryption processes,
and manages the interaction with the EnhancedSDES class.
"""

from typing import List, Tuple

from core.enhanced_sdes import EnhancedSDES
from utils.key_manager import KeyManager


class UserInterface:
    """
    A class to handle user interactions for the Enhanced S-DES encryption system.

    This class provides methods to guide the user through the encryption and decryption
    processes, handle user input, and interact with the EnhancedSDES class.

    Attributes:
        enhanced_sdes: An instance of EnhancedSDES.
        key_manager: An instance of KeyManager.
        saved_info: A dictionary to store encryption/decryption information.
    """

    def __init__(self) -> None:
        """
        Initialize the UserInterface instance.
        """
        self.enhanced_sdes = EnhancedSDES()
        self.key_manager = KeyManager()
        self.saved_info = {}

    def run(self) -> None:
        """
        Run the main loop of the user interface.
        """
        print("Welcome to the Enhanced S-DES Encryption System!")
        while True:
            choice = input("\nEnter 1 to encrypt, 2 to decrypt, or 3 to exit: ").lower()
            if choice == '1':
                self._encrypt_process()
            elif choice == '2':
                self._decrypt_process()
            elif choice == '3':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def _encrypt_process(self) -> None:
        """
        Guide the user through the encryption process.
        """
        while True:
            message = input("Enter the message to encrypt: ")
            if message:
                break
            print("Message cannot be empty. Please try again.")

        sdes_key = self._get_sdes_key()
        trans_key, column_size = self._get_transposition_key()

        rounds = int(input("Enter the number of transposition rounds (or press Enter for default 2): ") or 2)

        show_progress = input("Show encryption progress? (y/n): ").lower() == 'y'
        print("Encrypting ...\n")

        self.enhanced_sdes.set_show_progress(show_progress)
        ciphertext = self.enhanced_sdes.encrypt(message, sdes_key, trans_key, rounds)

        print(f"Encrypted message (hex): {ciphertext}")
        self._save_info(message, ciphertext, sdes_key, trans_key, column_size, rounds)

    def _decrypt_process(self) -> None:
        """
        Guide the user through the decryption process.
        """
        use_saved = self.saved_info and input("Use saved encryption info? (y/n): ").lower() == 'y'

        if use_saved:
            ciphertext = input("Enter the message to decrypt (hex): ")
            sdes_key = self.saved_info['sdes_key']
            trans_key = self.saved_info['trans_key']
            rounds = self.saved_info['rounds']
        else:
            ciphertext = input("Enter the message to decrypt (hex): ")
            sdes_key = self._get_sdes_key()
            trans_key, _ = self._get_transposition_key()
            rounds = int(input("Enter the number of transposition rounds: "))

        show_progress = input("Show decryption progress? (y/n): ").lower() == 'y'
        print("Decrypting ...\n")

        self.enhanced_sdes.show_progress = show_progress
        plaintext = self.enhanced_sdes.decrypt(ciphertext, sdes_key, trans_key, rounds)

        print(f"Decrypted message: {plaintext}")

    def _get_sdes_key(self) -> str:
        """
        Get or generate the S-DES key.

        Returns:
            The 10-bit S-DES key.
        """
        while True:
            sdes_key = input("Enter the 10-bit S-DES key (or press Enter to generate): ")
            if not sdes_key:
                sdes_key = self.key_manager.generate_sdes_key()
                print(f"Generated S-DES key: {sdes_key}")
                return sdes_key

            if self._validate_sdes_key(sdes_key):
                return sdes_key
            print("Invalid S-DES key. Please try again.")

    @staticmethod
    def _validate_sdes_key(key: str) -> bool:
        """
        Validate the S-DES key.

        Args:
            key: The S-DES key to validate.

        Returns:
            True if the key is valid, False otherwise.
        """
        return len(key) == 10 and all(bit in '01' for bit in key)

    def _get_transposition_key(self) -> Tuple[List[int], int]:
        """
        Get or generate the transposition key.

        Returns:
            A tuple containing the transposition key as a list of integers and the column size.
        """
        trans_key_input = input(
            "Enter the transposition key (space/comma-separated or [list] format, or press Enter to generate): "
        )

        if not trans_key_input:
            return self._generate_transposition_key()

        return self._parse_transposition_key(trans_key_input)

    def _generate_transposition_key(self) -> Tuple[List[int], int]:
        """
        Generate a transposition key based on user input or default value.

        Returns:
            A tuple containing the generated transposition key and column size.
        """
        column_size = self._get_column_size()
        trans_key = self.key_manager.generate_transposition_key(column_size)
        print(f"Generated transposition key: {trans_key}")

        return trans_key, column_size

    @staticmethod
    def _get_column_size() -> int:
        """
        Get the column size from user input or use the default value.

        Returns:
            The column size as an integer.

        Raises:
            ValueError: If the input is invalid.
        """
        while True:
            column_size_input = input("Enter column size (2-26, or press Enter for default): ")
            if not column_size_input:
                return 3
            try:
                column_size = int(column_size_input)
                if 2 <= column_size <= 26:
                    return column_size
                print("Column size must be between 2 and 26. Please try again.")

            except ValueError:
                print("Invalid input. Please enter a number between 2 and 26.")

    def _parse_transposition_key(self, key_input: str) -> Tuple[List[int], int]:
        """
        Parse the user-provided transposition key.

        Args:
            key_input: The user input string containing the transposition key.

        Returns:
            A tuple containing the parsed transposition key and column size.

        Raises:
            ValueError: If the key is invalid.
        """
        key_input = key_input.strip('[]')

        try:
            if ',' in key_input:
                trans_key = [int(k.strip()) for k in key_input.split(',')]
            else:
                trans_key = [int(k) for k in key_input.split()]

            if self._validate_transposition_key(trans_key):
                print(f"Transposition key accepted: {trans_key}")
                return trans_key, len(trans_key)

            raise ValueError("Invalid transposition key.")

        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
            return self._get_transposition_key()

    @staticmethod
    def _validate_transposition_key(trans_key: List[int]) -> bool:
        """
        Validate the transposition key for uniqueness and completeness.

        Args:
            trans_key: The transposition key as a list of integers.

        Returns:
            True if the key is valid, False otherwise.
        """
        if not (2 <= len(trans_key) <= 26):
            return False

        if len(set(trans_key)) != len(trans_key):
            return False

        if set(trans_key) != set(range(1, len(trans_key) + 1)):
            return False

        return True

    def _save_info(
            self,
            plaintext: str,
            ciphertext: str,
            sdes_key: str,
            trans_key: List[int],
            column_size: int,
            rounds: int
    ) -> None:
        """
        Save encryption information for later use.

        Args:
            plaintext: The plaintext message.
            ciphertext: The encrypted ciphertext.
            sdes_key: The S-DES key.
            trans_key: The transposition key.
            column_size: The number of columns in the transposition matrix.
            rounds: The number of transposition rounds.
        """
        self.saved_info = {
            'plaintext': plaintext,
            'ciphertext': ciphertext,
            'sdes_key': sdes_key,
            'trans_key': trans_key,
            'column_size': column_size,
            'rounds': rounds
        }

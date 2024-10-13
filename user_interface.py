"""
This module provides a user interface for the Enhanced S-DES encryption system.

It handles user input, guides the user through the encryption and decryption processes,
and manages the interaction with the EnhancedSDES class.
"""

from typing import List, Tuple

from enhanced_sdes import EnhancedSDES
from key_manager import KeyManager


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
        message = input("Enter the message to encrypt: ")
        sdes_key = self._get_sdes_key()
        trans_key, column_size = self._get_transposition_key()
        rounds = int(input("Enter the number of transposition rounds: "))
        show_progress = input("Show encryption progress? (y/n): ").lower() == 'y'
        print("Encrypting ...\n")

        self.enhanced_sdes.show_progress = show_progress
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
        sdes_key = input("Enter the 10-bit S-DES key (or press Enter to generate): ")
        if not sdes_key:
            sdes_key = self.key_manager.generate_sdes_key()
            print(f"Generated S-DES key: {sdes_key}")
        return sdes_key

    def _get_transposition_key(self) -> Tuple[List[int], int]:
        """
        Get or generate the transposition key.

        Accepts the following formats:
        - Space-separated: 1 2 3
        - Comma-separated (with or without spaces): 1,2,3 or 1, 2, 3
        - List format (with or without spaces): [1,2,3] or [1, 2, 3]

        Returns:
            A tuple containing the transposition key as a list of integers and the column size.
        """
        print("Enter the transposition key in one of the following formats:")
        print("- Space-separated: 1 2 3")
        print("- Comma-separated: 1,2,3")
        print("- List format: [1,2,3]")
        trans_key_input = input("Enter the transposition key (or press Enter to generate): ")
        if trans_key_input:
            trans_key_input = trans_key_input.strip('[]')

            if ',' in trans_key_input:
                # Comma-separated format
                trans_key = [int(k.strip()) for k in trans_key_input.split(',')]
            else:
                # Space-separated format
                trans_key = [int(k) for k in trans_key_input.split()]

            column_size = len(trans_key)
            print(f"Transposition key accepted: {trans_key}")
        else:
            column_size_input = input("Enter column size (2-26, or press Enter for default): ")
            column_size = int(column_size_input) if column_size_input else 5
            trans_key = self.key_manager.generate_transposition_key(column_size)
            print(f"Generated transposition key: {trans_key}")

        return trans_key, column_size

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

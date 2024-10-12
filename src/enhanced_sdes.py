from column_transposition import ColumnTransposition
from key_manager import KeyManager
from sdes import SDES
from shift_rows import ShiftRows


class EnhancedSDES:
    def __init__(self, show_progress=False):
        self.show_progress = show_progress
        self.transposition = ColumnTransposition()
        self.shift_rows = ShiftRows()
        self.sdes = SDES()
        self.key_manager = KeyManager()

    def encrypt(self, plaintext, sdes_key, trans_key, rounds):
        # TODO: Implement encryption
        pass

    def decrypt(self, ciphertext, sdes_key, trans_key, rounds):
        # TODO: Implement decryption
        pass

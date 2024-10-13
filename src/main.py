"""
Main entry point for the Enhanced S-DES encryption system.

This script initializes and runs the user interface for the encryption system.
"""

from user_interface import UserInterface


def main() -> None:
    """
    Initialize and run the user interface.
    """
    ui = UserInterface()
    ui.run()


if __name__ == "__main__":
    main()

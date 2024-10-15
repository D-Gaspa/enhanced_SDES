"""
This module defines the ProgressLevel enumeration for the Enhanced S-DES encryption system.

The ProgressLevel enum is used to control the verbosity of output during the encryption
and decryption processes, allowing users to choose between different levels of detail
in the progress information displayed.
"""

from enum import Enum


class ProgressLevel(Enum):
    """
    An enumeration of progress output levels for the Enhanced S-DES encryption system.

    This enum defines three levels of progress output:
    - NONE: No progress information is displayed.
    - NORMAL: Basic progress information is displayed, showing the main steps of the process.
    - DETAILED: Comprehensive progress information is displayed, including intermediate steps.

    These levels can be used to control the verbosity of output in various components
    of the encryption system, allowing users to choose their preferred level of detail.

    Attributes:
        NONE (int):     Represents no progress output (value: 0).
        NORMAL (int):   Represents normal progress output with main steps (value: 1).
        DETAILED (int): Represents detailed progress output with all steps (value: 2).
    """
    NONE = 0
    NORMAL = 1
    DETAILED = 2

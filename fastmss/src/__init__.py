"""
Blazing fast multi-monitor screen capture. Updates the Windows capture method to be ~3x faster.

Uses mss (https://github.com/BoboTiG/python-mss) on Mac and Linux.
Uses DXcam (https://github.com/ra1nty/DXcam) on Windows, modifying the API into mss's style.
"""
from mss.exception import ScreenShotError
from .factory import mss
from mss import *

__version__ = "1.0.0"
__author__ = "Giantpizzahead"

__all__ = ("ScreenShotError", "mss", "tools")

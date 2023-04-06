"""
This is part of the MSS Python's module.
Source: https://github.com/BoboTiG/python-mss
"""
import platform
from typing import Any

from mss.base import MSSBase
from mss.exception import ScreenShotError


def mss(**kwargs: Any) -> MSSBase:
    """Factory returning a proper MSS class instance.
    Note: There are important optimization arguments for Windows (FastMSS)!
    Namely, video_mode (bool), target_fps (int), and region (tuple).
    See the docs for more information.

    It detects the platform we are running on
    and chooses the most adapted mss_class to take
    screenshots.
    It then proxies its arguments to the class for
    instantiation.
    """
    # pylint: disable=import-outside-toplevel

    os_ = platform.system().lower()

    if os_ == "darwin":
        from mss import darwin

        return darwin.MSS(**kwargs)

    if os_ == "linux":
        from mss import linux

        return linux.MSS(**kwargs)

    if os_ == "windows":
        from . import windows_fast

        return windows_fast.MSS(**kwargs)

    raise ScreenShotError(f"System {os_!r} not (yet?) implemented.")
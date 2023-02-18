"""
Modified version of MSS's Windows implementation, using DXcam for screenshots instead.
"""

from typing import Any

from mss.windows import MSS as MSSWindows
from mss.base import ScreenShot, ScreenShotError, Monitor
import dxcam


class MSS(MSSWindows):
    """ Faster MSS Windows implementation using DXcam. """

    def __init__(self, **_: Any) -> None:
        """Windows initialisations."""
        super().__init__()
        self.camera = dxcam.create()

    def _grab_impl(self, monitor: Monitor) -> ScreenShot:
        """
        Retrieve all pixels from a monitor. Pixels have to be RGB.
        In the code, there are a few interesting things:
        [1] bmi.bmiHeader.biHeight = -height
        A bottom-up DIB is specified by setting the height to a
        positive number, while a top-down DIB is specified by
        setting the height to a negative number.
        https://msdn.microsoft.com/en-us/library/ms787796.aspx
        https://msdn.microsoft.com/en-us/library/dd144879%28v=vs.85%29.aspx
        [2] bmi.bmiHeader.biBitCount = 32
            image_data = create_string_buffer(height * width * 4)
        We grab the image in RGBX mode, so that each word is 32bit
        and we have no striding.
        Inspired by https://github.com/zoofIO/flexx
        [3] bmi.bmiHeader.biClrUsed = 0
            bmi.bmiHeader.biClrImportant = 0
        When biClrUsed and biClrImportant are set to zero, there
        is "no" color table, so we can read the pixels of the bitmap
        retrieved by gdi32.GetDIBits() as a sequence of RGB values.
        Thanks to http://stackoverflow.com/a/3688682
        """

        left, top, width, height = monitor["left"], monitor["top"], monitor["width"], monitor["height"]
        print(left, top, width, height, monitor, self._bbox)
        # if (self._bbox["height"], self._bbox["width"]) != (height, width):
        #     self._bbox = monitor
        #     self._data = ctypes.create_string_buffer(width * height * 4)  # [2]
        # bits = self.gdi32.GetDIBits(
        #     memdc, MSS.bmp, 0, height, self._data, self._bmi, DIB_RGB_COLORS
        # )
        # if bits != height:
        #     raise ScreenShotError("gdi32.GetDIBits() failed.")

        return self.cls_image(bytearray([255, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 0]), monitor)
"""
Modified version of MSS's Windows implementation, using DXcam for screenshots instead.
"""

from typing import Any, Union, Tuple

from mss.windows import MSS as MSSWindows
from mss.base import ScreenShot, ScreenShotError, Monitor
import dxcam
import numpy as np
import time


class MSS(MSSWindows):
    """Faster MSS Windows implementation using DXcam.
    
    This implementation uses DXcam to take screenshots, instead of GDI.
    It is much faster, but also uses more resources.
    Only use this if you're planning to take a LOT of screenshots (say, at least 20 per second)!
    """

    def __init__(self, video_mode=False, target_fps=60, region=None, device_idx=0, output_idx=None) -> None:
        """Windows initialisations.

        Args:
            video_mode: Whether to continuously take screenshots, or only take them when requested.
                If False, grab() will take screenshots on demand. Note that due to caching, this method
                could return almost instantly (if the frame hasn't changed), or it could take a while.
                For a more consistent frame rate, turn on video_mode and set the target_fps.
                If True, grab() will return the last *ready* screenshot. This will be much faster,
                but will use much more resources, and the frame returned could be a bit out of date.
            target_fps: The target FPS. Defaults to 60.
                FastMSS will try to take 1 new screenshot every (1/target_fps) seconds.
                Don't set this too high, Python might hang if it can't keep up!
                Has no effect if video_mode is False.
            region: The region to continuously capture, as a tuple (left, top, right, bottom).
                Captures the whole screen by default.
                Has no effect if video_mode is False.
            device_idx: The index of the device to use. See DXcam docs.
            output_idx: The index of the output to use. See DXcam docs.
        """
        super().__init__()
        self.target_fps = target_fps
        self.video_mode = video_mode
        self.camera = dxcam.create(device_idx=device_idx, output_idx=output_idx, output_color="BGRA")
        if self.video_mode:
            self.camera.start(region=region, target_fps=target_fps, video_mode=True)
            self.video_region = region or (0, 0, self.camera.width, self.camera.height)
        else:
            self.prev_frame = self._dxcam_force_grab((0, 0, self.camera.width, self.camera.height))
            self.prev_region = (0, 0, self.prev_frame.shape[1], self.prev_frame.shape[0])
            self.prev_frame = self._convert_frame(self.prev_frame)
    
    def _convert_frame(self, frame):
        """Convert the frame to the right format (flattened bytes)."""
        return frame.flatten().tobytes()

    def _dxcam_force_grab(mss_self, region: Tuple[int, int, int, int]):
        """Force a screenshot to be taken, even if DXcam thinks the frame hasn't changed."""
        self = mss_self.camera
        if self._duplicator.update_frame():
            if self._duplicator.updated:
                self._device.im_context.CopyResource(
                    self._stagesurf.texture, self._duplicator.texture
                )
                self._duplicator.release_frame()
            rect = self._stagesurf.map()
            frame = self._processor.process(
                rect, self.width, self.height, region, self.rotation_angle
            )
            self._stagesurf.unmap()
            return frame
        else:
            self._on_output_change()
            return mss_self._dxcam_force_grab(region)

    def _grab_impl(self, monitor: Monitor) -> ScreenShot:
        """
        Retrieve all pixels from a monitor. Pixels have to be RGB.
        Note: The returned raw pixels are not writeable!
        """

        left, top, width, height = monitor["left"], monitor["top"], monitor["width"], monitor["height"]
        right = left + width
        bottom = top + height
        region = (left, top, right, bottom)
        if self.video_mode:
            # Only allow portions of the video region to be captured
            if (region[0] < self.video_region[0] or region[1] < self.video_region[1] or
                region[2] > self.video_region[2] or region[3] > self.video_region[3]):
                raise ScreenShotError("Cannot capture outside the video region passed to mss.mss()")
            curr_frame = self.camera.get_latest_frame()
            # Crop to region and convert to bytes
            curr_frame = curr_frame[region[1]:region[3], region[0]:region[2]]
            curr_frame = self._convert_frame(curr_frame)
        else:
            # Get current frame
            used_cache = False
            if region == self.prev_region:
                curr_frame = self.camera.grab(region=region)
                if curr_frame is None:
                    used_cache = True
                    curr_frame = self.prev_frame
                else:
                    curr_frame = self._convert_frame(curr_frame)
            else:
                curr_frame = self._convert_frame(self._dxcam_force_grab(region))

            # Save copy to previous frame
            if not used_cache:
                self.prev_frame = curr_frame
                self.prev_region = region
        
        return self.cls_image(curr_frame, monitor)
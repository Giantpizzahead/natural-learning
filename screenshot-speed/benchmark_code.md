## Benchmark Code

```python
""" =============================== Pillow  =============================== """
from PIL import ImageGrab
def get_screenshot():
    return ImageGrab.grab(bbox=BBOX)


""" ===============================   MSS   =============================== """
import mss
import numpy as np
sct = mss.mss()
def get_screenshot():
    return np.asarray(sct.grab(sct.monitors[0] if not BBOX else BBOX))


""" ===============================  DXcam  =============================== """
import dxcam
camera = dxcam.create()
# Video mode was turned to False for the UFO 60FPS test to test
# DXcam's raw video capture speed, without cache optimizations.
camera.start(target_fps=0, video_mode=True, region=BBOX)
def get_screenshot():
    return camera.get_latest_frame()


""" =============================== np.sum  =============================== """
import numpy as np
screenshot = np.asarray("Taken using MSS, not counted in time taken")
def get_screenshot():
    # Simulating iteration over all pixels
    total = screenshot.sum()
    print("Sum of pixel values:", total)
    return screenshot
```

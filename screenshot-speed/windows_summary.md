## Windows

TLDR; Use [DXcam](https://github.com/ra1nty/DXcam). Expect ~100 FPS for mid tier PCs.

DXcam grabs the raw screen faster, and has optimizations if the image doesn't always change. [MSS](https://github.com/BoboTiG/python-mss) is fine for cross-platform and ease of use, but will be about 3 times slower on Windows.

### Results

FPS is displayed as mean ± σ. Results on a mid tier 1920x1200 Windows laptop:

| Test Type    | Pillow         | MSS            | DXcam             | np.sum(screen) |
| ------------ | -------------- | -------------- | ----------------- | -------------- |
| Static       | 27 ± 0.5       | 29 ± 0.1       | **170 ± 3.4\***   | ~650           |
| Dynamic      | 22 ± 1.4       | 28 ± 0.7       | **96 ± 9.2\***    | ~650           |
| UFO 60FPS    | ~19            | ~25            | **~60**           | ~650           |
| Small Region | 27 ± 0.7       | 57 ± 0.3       | **387 ± 11.4\***  | ~5000          |

np.sum(screen) serves as a baseline. It measures how many times Numpy can iterate through the whole image in one second.

\*See details.

### Details

DXcam has a lot of optimizations, including only processing / outputting new frames when something's changed (along with a "video mode" that kind of? controls this feature). This makes it hard to compare with the others objectively. But overall, DXcam is much faster than both of the other options, both in terms of capturing the raw screen and real usage. So just use it on Windows.

Use MSS on Mac and Linux (maybe Windows to trade ease of use with a noticeable speed decrease) if you need cross compatability.

The above FPS values aren't 100% accurate, due to minor testing issues / oversights. The overall trend is definitely right though.
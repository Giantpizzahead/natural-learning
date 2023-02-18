## Mac

TLDR; Use [MSS](https://github.com/BoboTiG/python-mss). ~50 FPS on a MacBook Air (M1, 2020).

MSS is 15-20 times faster than Pillow, and I couldn't find any better options. It can also be sped up by grabbing specific screen regions.

### Results

FPS is displayed as mean ± σ. Results on an MacBook Air (M1, 2020):

| Test Type    | Pillow         | MSS            | np.sum(screen) |
| ------------ | -------------- | -------------- | -------------- |
| Dynamic      | 2.8 ± 0.0      | **47 ± 1.2**   | 260 ± 7.0      |
| Small Region | 2.6 ± 0.1      | **61 ± 1.1**   | 639 ± 47       |

np.sum(screen) serves as a baseline. It measures how many times Numpy can iterate through the whole image in one second.

Both static and dynamic screens were tested, but the results were very similar (neither library optimizes for still images), so I only included the dynamic results.

### Details

So, Mac has a Retina display, which means the displayed resolution is doubled from
the *virtual* resolution. That is, for all intents and purposes, treat a 2800 x 1800
Mac screen as 1400 x 900. (The retina part is ONLY for making the display look better.)

Virtual = Normal resolution, Retina = Double resolution
Both screenshot libraries use virtual resolution to specify the desired region to grab.
Then they used different methods to handle the retina resolution:

Pillow - If no region is specified, Pillow uses (0, 0, retina width, retina height).
First, Pillow uses screencapture (Mac commandline tool) to grab the *virtual resolution* region
of the screen, returning that region in *retina resolution*. Then, Pillow resizes that image into
the specified region size, and returns it. All in all, you specify a virtual res size, and Pillow
returns an image of that virtual res size. But if you don't specify a region, a retina res version
of the screen is returned.

MSS - If no region is specified, MSS uses (0, 0, virtual width, virtual height).
Luckily, MSS is straightforward. Query a virtual res region, and the returned image will be retina res.

Basically, just use MSS. I'm noting down the technical details here for completeness's sake.

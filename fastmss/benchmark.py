"""
Benchmark for FastMSS.
Ran with TestUFO on fullscreen.
(https://www.testufo.com/framerates#count=6&background=stars&pps=1440)
"""
import time
start_time = time.time()

import fastmss as mss

import timeit
from random import randint

START_DELAY = 0.5
N = 240
# FastMSS optimizes for the common use case of always grabbing the same region
# This option "disables" that optimization to make the benchmark more fair
NO_CACHING = True

# MSS, FastMSS without video mode
# sct = mss.mss()
# FastMSS with video mode
sct = mss.mss(video_mode=False, target_fps=144)

# Do initial setup without affecting the benchmark
w, h = sct.monitors[1]["width"], sct.monitors[1]["height"]
print(f"Starting in {START_DELAY} seconds...")
while time.time() < start_time + START_DELAY:
    pass
print("Starting now!")

def entire_screen():
    img = sct.grab(sct.monitors[1])
    if NO_CACHING:
        sct.grab((0, 0, 1, 1))
    return img

fps = N / timeit.timeit(entire_screen, number=N)
print(f"Entire screen FPS: {fps:.2f}")

def random_regions():
    qw, qh = randint(0, w), randint(0, h)
    ql, qt = randint(0, w-qw), randint(0, h-qh)
    return sct.grab((ql, qt, ql+qw, qt+qh))

fps = N / timeit.timeit(random_regions, number=N)
print(f"Random regions FPS: {fps:.2f}")

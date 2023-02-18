"""
Calculates FPS from benchmark info.
Everything is in milliseconds!
All pairs are (mean, std_dev).
"""

import math

NUM_FRAMES = 360
BASELINE = (600, 5)
TO_CONVERT = [
    (14006, 343),
    (6879, 27),
    (1532, 27)
]

def get_actual_time(time):
    new_time = (time[0] - BASELINE[0]), math.sqrt(BASELINE[1]**2 + time[1]**2)
    return new_time

def get_fps(time: tuple):
    time_per_frame = [n / NUM_FRAMES for n in time]
    min_fps = 1000 / (time_per_frame[0] + time_per_frame[1])
    max_fps = 1000 / (time_per_frame[0] - time_per_frame[1])
    return (min_fps+max_fps)/2, (max_fps-min_fps)/2

for time in TO_CONVERT:
    result = get_fps(get_actual_time(time))
    print(f"{result[0]:.1f} ± {result[1]:.1f}")

"""
Using DXcam to take screenshots. Only works on Windows.
"""

import time
start_time = time.time()

START_DELAY = 0.5
NUM_FRAMES = 120
BBOX = None
# BBOX = (1920//2-256, 1200//2-256, 1920//2+256, 1200//2+256)
COUNT_UNIQUE = False
DEBUG = False

# =============================================================================
# BEGIN SCREENSHOT CODE
# =============================================================================

import dxcam
import numpy as np
camera = dxcam.create()
camera.start(target_fps=0, video_mode=False, region=BBOX)
print("Screen:", camera.get_latest_frame().shape[:2][::-1])


def get_screenshot():
    return camera.get_latest_frame()
    # while True:
    #     img = camera.grab(region=BBOX)
    #     if img is not None:
    #         return img

# =============================================================================
# END SCREENSHOT CODE
# =============================================================================

import cv2


# Make sure initial setup doesn't affect the benchmark
def delay_start():
    print(f"Starting in {START_DELAY} seconds...")
    while time.time() < start_time + START_DELAY:
        pass
    print("Starting now!")


def get_time_elapsed():
    return time.time() - start_time - START_DELAY


def main():
    delay_start()

    # Run the test
    unique = set() if COUNT_UNIQUE else None
    for i in range(NUM_FRAMES):
        img = get_screenshot()
        if DEBUG:
            # Show screenshot with FPS in red
            to_display = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            to_display = cv2.resize(to_display, (0, 0), fx=0.5, fy=0.5)
            cv2.putText(to_display, f"FPS: {(i+1) / get_time_elapsed():.2f}",
                        (10, 33), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Screen", to_display)
            
            cv2.waitKey(1)
        if COUNT_UNIQUE:
            unique.add(img.tobytes())
    
    # Print results
    time_taken = get_time_elapsed()
    print(f"FPS: {NUM_FRAMES / time_taken:.2f}")
    print(f"Time taken: {time_taken:.2f}s")
    if COUNT_UNIQUE:
        print(f"Unique frames: {len(unique)}/{NUM_FRAMES}")
    if COUNT_UNIQUE or DEBUG:
        print("WARNING: Debug options are on, benchmark will be inaccurate!")


if __name__ == "__main__":
    main()

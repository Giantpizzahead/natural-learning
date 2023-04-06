import mss
import cv2
import numpy as np
import time
import random

sct = mss.mss(target_fps=144, video_mode=False, region=(1, 1, 1920, 1200))
print(sct)
print(sct.monitors)

img = sct.grab(sct.monitors[0])
cv2.imwrite("test1.png", np.asarray(img))

img = sct.grab((500, 100, 1012, 356))
cv2.imwrite("test2.png", np.asarray(img))

print(img.rgb[:20])
print(img.bgra[:20])
print(img.pixel(2, 2))
img = sct.grab((1000, 300, 1200, 600))
cv2.imwrite("test3.png", np.asarray(img))

N = 1000

start = time.time()
for i in range(1, N+1):
    if i % 100 == 0: print(i, time.time() - start)
    # img = sct.grab((random.randint(0, 1), random.randint(0, 1), random.randint(2, 3), random.randint(2, 3)))
    img = sct.grab((random.randint(0, 100), random.randint(0, 100), random.randint(1820, 1920), random.randint(1100, 1200)))
    img = np.asarray(img)
print("Random regions FPS:", N / (time.time() - start))

start = time.time()
for i in range(1, N+1):
    if i % 100 == 0: print(i, time.time() - start)
    img = sct.grab(sct.monitors[1])
    img = np.asarray(img)
    sct.grab((0, 0, 1, 1))  # To force a new screenshot to be taken (no caching)
print("Entire screen FPS:", N / (time.time() - start))

import fastmss as mss
import cv2

sct = mss.mss()
print(sct)
print(sct.monitors)
img = sct.grab(sct.monitors[0])
cv2.imshow('test', img)
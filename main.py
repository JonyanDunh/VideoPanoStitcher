import stitching
from stitching import Stitcher
from stitching import AffineStitcher
import os
from PIL import Image
import matplotlib.pyplot as plt
import time
import cv2
import numpy as np
# 读取视频文件
# videoCapture1 = cv2.VideoCapture("video/video_pano1.mp4")
# success1, frame1 = videoCapture1.read()
# videoCapture2 = cv2.VideoCapture("video/video_pano2.mp4")
# success2, frame2 = videoCapture2.read()
# cv2.imwrite("image/1.jpg",frame1)
# cv2.imwrite("image/2.jpg",frame2)
print('first:')
time_start = time.time()
settings = {  # The whole plan should be considered
    "crop": False,
    # The matches confidences aren't that good
    "confidence_threshold": 0.5}
stitcher = AffineStitcher(**settings)
panorama = stitcher.stitch(["video/video_pano1.mp4", "video/video_pano2.mp4", "video/video_pano3.mp4", "video/video_pano4.mp4"])
time_end = time.time()
print('all time cost', time_end - time_start, 's')
plt.imshow(panorama)
plt.show()

print('secondly:')
time_start = time.time()
panorama = stitcher.stitch(["video/video_pano1.mp4", "video/video_pano2.mp4", "video/video_pano3.mp4", "video/video_pano4.mp4"])
time_end = time.time()
print('all time cost', time_end - time_start, 's')
plt.imshow(panorama)
plt.show()

print('thirdly:')
time_start = time.time()
panorama = stitcher.stitch(["video/video_pano1.mp4", "video/video_pano2.mp4", "video/video_pano3.mp4", "video/video_pano4.mp4"])
time_end = time.time()
print('all time cost', time_end - time_start, 's')
plt.imshow(panorama)
plt.show()



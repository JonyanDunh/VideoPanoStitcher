import stitching
from stitching import Stitcher
from stitching import AffineStitcher
import os
from PIL import Image
import matplotlib.pyplot as plt
import time
import cv2
import numpy as np
settings = {"crop": False,"confidence_threshold": 0.5}
stitcher = AffineStitcher(**settings)
VideoCaptureArray=[cv2.VideoCapture("video/video_pano1.mp4"),
                   cv2.VideoCapture("video/video_pano2.mp4"),
                   cv2.VideoCapture("video/video_pano3.mp4"),
                   cv2.VideoCapture("video/video_pano4.mp4")]
time_start = time.time()
for t in range(10):
    for ChildId in range(5):
        for fps in range(5):
            FpsArray=[]
            fps_time_start = time.time()
            for VideoId in range(4):
                FpsArray.append(VideoCaptureArray[VideoId].read())
            panorama = stitcher.stitch(
                ["video/video_pano1.mp4", "video/video_pano2.mp4", "video/video_pano3.mp4", "video/video_pano4.mp4"],FpsArray)
            cv2.imshow('frame', panorama)
            if cv2.waitKey(1) == ord('q'):
                break
            fps_time_end = time.time()
            print('per fps time cost', fps_time_end - fps_time_start, 's')
time_end = time.time()
print('all time cost', time_end - time_start, 's')



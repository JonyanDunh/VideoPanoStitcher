import stitching
from stitching import Stitcher
from stitching import AffineStitcher
import os
from PIL import Image
import matplotlib.pyplot as plt
import time
import cv2
import numpy as np
import threading
from multiprocessing import Process
from threading import Thread
thread_num=1
PanoramaArray = [None] * thread_num

features=None
matches=None
def runStitcher(threadID, FpsArray):
    global features
    global matches
    settings = {"crop": False, "confidence_threshold": 0.5}
    stitcher = AffineStitcher(**settings)
    panorama,tmp_features,tmp_matches = stitcher.stitch(
        FpsArray[threadID],features,matches)
    if (features is None) and (matches is None):
        features=tmp_features
        matches=tmp_matches
    PanoramaArray[threadID] = panorama
VideoCaptureArray = [cv2.VideoCapture("video/video_pano1.mp4"),
                     cv2.VideoCapture("video/video_pano2.mp4"),
                     cv2.VideoCapture("video/video_pano3.mp4"),
                     cv2.VideoCapture("video/video_pano4.mp4")]
if __name__ == '__main__':
    time_start = time.time()
    for t in range(1):
        for ChildId in range(100):
            FpsArray = []
            fps_time_start = time.time()
            for fps in range(thread_num):
                subFpsArray=[]
                for VideoId in range(4):
                    subFpsArray.append(VideoCaptureArray[VideoId].read())
                FpsArray.append(subFpsArray)
            thread_list = [None] * thread_num
            for i in range(thread_num):
                thread_list[i]=Thread(target=runStitcher, args=(i, FpsArray))
                thread_list[i].start()

            for thread in thread_list:
                thread.join()
            thread_num = len(threading.enumerate())
            print("主线程：线程数量是%d" % thread_num)

            for panorama in PanoramaArray:
                # cv2.imwrite("output/" + str(time.time())+".jpg", panorama)
                cv2.imshow('frame', panorama)
            if cv2.waitKey(1) == ord('q'):
                break
            fps_time_end = time.time()
            print('per two fps time cost', fps_time_end - fps_time_start, 's')
    time_end = time.time()
    print('all time cost', time_end - time_start, 's')

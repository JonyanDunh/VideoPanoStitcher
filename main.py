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
from numba import jit
thread_num=1
features=None
matches=None
seam_masks=None

def runStitcher(threadID, FpsArray):
    global features
    global matches
    global seam_masks
    settings = {"crop": False, "confidence_threshold": 0.5}
    stitcher = AffineStitcher(compensator="no",**settings, blender_type="no")
    panorama,tmp_features,tmp_matches,tmp_seam_masks = stitcher.stitch(
        FpsArray,features,matches,seam_masks)
    if (features is None) and (matches is None):
        features=tmp_features
        matches=tmp_matches
        seam_masks=tmp_seam_masks
    return panorama
VideoCaptureArray = [cv2.VideoCapture("video/video_pano1.mp4"),
                     cv2.VideoCapture("video/video_pano2.mp4"),
                     cv2.VideoCapture("video/video_pano3.mp4"),
                     cv2.VideoCapture("video/video_pano4.mp4")]
class ThreadWithReturnValue(Thread):
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self):
        super().join()
        return self._return
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
            thread_list = []
            for i in range(thread_num):
                thread_list.append(ThreadWithReturnValue(target=runStitcher, args=(i, FpsArray[i])))
            for thread in thread_list:
                thread.start()
            for thread in thread_list:
                thread.join()

                # cv2.imshow('frame', thread.join())
            if cv2.waitKey(1) == ord('q'):
                break
            fps_time_end = time.time()
            print('per '+str(thread_num)+' fps time cost', fps_time_end - fps_time_start, 's')
    time_end = time.time()
    print('all time cost', time_end - time_start, 's')

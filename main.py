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

thread_num = 1
features = None
matches = None
seam_masks = None


def runStitcher(threadID, FpsArray):
    global features
    global matches
    global seam_masks
    settings = {"crop": False, "confidence_threshold": 0.55}
    stitcher = AffineStitcher(compensator="no", **settings, blender_type="no")
    panorama, tmp_features, tmp_matches, tmp_seam_masks = stitcher.stitch(
        FpsArray, features, matches, seam_masks)
    if (features is None) and (matches is None):
        features = tmp_features
        matches = tmp_matches
        seam_masks = tmp_seam_masks
    # print(panorama.shape)
    return panorama


# VideoCaptureArray = [cv2.VideoCapture("video/video_pano1.mp4"),
#                      cv2.VideoCapture("video/video_pano2.mp4"),
#                      cv2.VideoCapture("video/video_pano3.mp4"),
#                      cv2.VideoCapture("video/video_pano4.mp4")]
VideoCaptureArray = [cv2.VideoCapture("rtsp://192.168.1.9:554/user=admin&password=&channel=1&stream=0.sdp?real_stream--rtp-caching=100"),
                     cv2.VideoCapture("rtsp://192.168.1.197:554/user=admin&password=&channel=1&stream=0.sdp?real_stream--rtp-caching=100"),
                     cv2.VideoCapture("rtsp://192.168.1.10:554/user=admin&password=&channel=1&stream=0.sdp?real_stream--rtp-caching=100"),
                     cv2.VideoCapture("rtsp://192.168.1.17:554/user=admin&password=&channel=1&stream=0.sdp?real_stream--rtp-caching=100")]


class ThreadWithReturnValue(Thread):
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        super().join()
        return self._return


if __name__ == '__main__':
    time_start = time.time()

    # videowriter = cv2.VideoWriter('output/video2.avi', cv2.VideoWriter_fourcc(*'MJPG'), 23, (992, 558))
    for t in range(1):
        # for ChildId in range(100):
        while True:
            FpsArray = []
            fps_time_start = time.time()
            for fps in range(thread_num):
                subFpsArray = []
                for VideoId in range(4):
                    subFpsArray.append(VideoCaptureArray[VideoId].read())
                FpsArray.append(subFpsArray)
            thread_list = []
            for i in range(thread_num):
                thread_list.append(ThreadWithReturnValue(target=runStitcher, args=(i, FpsArray[i])))
            for thread in thread_list:
                thread.start()
            for thread in thread_list:
                Video=thread.join()
                # videowriter.write(Video)
                # thread.join()
                cv2.imshow('frame', Video)
                cv2.waitKey(1)
            fps_time_end = time.time()
            print('fps ', 1 / (fps_time_end - fps_time_start))
    time_end = time.time()
    print('all time cost', time_end - time_start, 's')

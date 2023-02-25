import stitching
from stitching import Stitcher
from stitching import AffineStitcher
import os
from PIL import Image
import matplotlib.pyplot as plt
import time

time_start=time.time()


settings = {# The whole plan should be considered
            "crop": False,
            # The matches confidences aren't that good
            "confidence_threshold": 0.5}

stitcher = AffineStitcher(**settings)
# panorama = stitcher.stitch(["library/1.jpg","library/2.jpg","library/3.jpg"
#                             ,"library/4.jpg","library/5.jpg","library/6.jpg"
#                             ,"library/7.jpg","library/8.jpg","library/9.jpg"
#                             ,"library/10.jpg","library/11.jpg","library/12.jpg"
#                             ,"library/13.jpg"])
panorama = stitcher.stitch(["test2/1.jpg","test2/2.jpg","test2/3.jpg"])
time_end=time.time()
print('time cost',time_end-time_start,'s')
print(panorama.shape)


plt.imshow(panorama)
plt.show()

import RPi.GPIO as GPIO

from picamera.array import PiRGBArray
from picamera import PiCamera
import time

#import cv2
#print(cv2.__version__)

import numpy as np
print(np.__version__)
print(np.__path__)
import numpy.core.multiarray
import pandas as pd
print(pd.__version__)
import opencv_color_detect as PROCESS
#import decision_tree as det


def begin_capture():
	camera=PiCamera()
	camera.resolution=(640,480)
	camera.framerate=50
	camera.hflip=True

	rawCapture=PiRGBArray(camera,size=(640,480))

	time.sleep(0.1)
	print("starting camera...")
	MODE=0

	for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
		#key=cv2.waitKey(1) & 0xFF
		images=PROCESS.process_image(frame.array)

		#print("HERE")
		rawCapture.truncate(0)
		time.sleep(0.1)
		#rawCapture.seek(0)#

begin_capture()



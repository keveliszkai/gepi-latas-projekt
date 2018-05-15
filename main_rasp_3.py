# import the necessary packages
from multiprocessing import Process
import subprocess
import argparse
import datetime
import imutils
import time
import cv2
import os

min_area = 500
min_delay = 0.02

current_folder = os.getcwd()
database_folder = os.getcwd()

if __name__ == '__main__':

	# initialize the first frame in the video stream
	firstFrame = None

	camera = cv2.VideoCapture(0)
	time.sleep(0.25)
	change = False

	wait = Process(target=time.sleep, args=(1,))
	wait.start()

	# loop over the frames of the video
	while True:
		# grab the current frame
		(grabbed, frame) = camera.read()

		# if the frame could not be grabbed, then we have reached the end
		# of the video
		if not grabbed:
			break

		# resize the frame, convert it to grayscale, and blur it
		frame = imutils.resize(frame, width=500)
		#frame = cv2.flip(frame, 0)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)

		# if the first frame is None, initialize it
		if firstFrame is None:
			firstFrame = gray
			continue

		# compute the absolute difference between the current frame and
		# first frame
		frameDelta = cv2.absdiff(firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

		# dilate the thresholded image to fill in holes, then find contours
		# on thresholded image
		thresh = cv2.dilate(thresh, None, iterations=2)
		(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)

		# loop over the contours
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < min_area:
				continue
		
			# There is change
			change = True

		# draw the text and timestamp on the frame
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		cv2.putText(frame, "", (10, 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		cv2.putText(frame, date,
			(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		key = cv2.waitKey(1) & 0xFF

		#firstFrame = gray

		if (wait.exitcode != None):
			firstFrame = gray
			if (change):
				# Archive
				cv2.imwrite(date+'_o.png',frame)
				change = False
				print("CHANGE")
			else:
				print("NO CHANGE")
			wait = Process(target=time.sleep, args=(5,))
			wait.start()

		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break

		
		time.sleep(min_delay)

	# cleanup the camera and close any open windows
	camera.release()
	cv2.destroyAllWindows()

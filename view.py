# USAGE
# python motion_detector.py

# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2

# if the video argument is None, then we are reading from webcam
camera = cv2.VideoCapture(0)
time.sleep(0.25)

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

	# draw the text and timestamp on the frame
	cv2.putText(frame, "", (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# Camera
	cv2.imshow("Camera", frame)

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

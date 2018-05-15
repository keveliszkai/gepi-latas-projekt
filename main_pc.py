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
darknet_folder = "/home/osboxes/darknet-master/"
darknet_config = "cfg/yolov3.cfg"
darknet_weights = "yolov3.weights"

def checkImage(frame, date):
	print("START - "+datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"))
	command = ["./darknet", "detect", darknet_config, darknet_weights, current_folder + "/img.png", "/dev/null"]
	p = subprocess.Popen(command, cwd=darknet_folder, stdout=subprocess.PIPE)
	p.wait()
	output = p.stdout.read().decode("utf-8")
	print("Output: "+output)

	# cat
	if "cat" in output:
		cv2.imwrite(database_folder + '/cat/' + date + '_o.png',frame)
		command = ['cp', darknet_folder + 'predictions.png', database_folder + '/cat/' + date + '.png']
		subprocess.run(command)
		print("cat")
	# dog
	elif "dog" in output:
		cv2.imwrite(database_folder + '/dog/' + date + '_o.png',frame)
		command = ['cp', darknet_folder + 'predictions.png', database_folder + '/dog/' + date + '.png']
		subprocess.run(command)
		print("dog")
	# person
	elif "person" in output:
		cv2.imwrite(database_folder + '/person/' + date + '_o.png',frame)
		command = ['cp', darknet_folder + 'predictions.png', database_folder + '/person/' + date + '.png']
		subprocess.run(command)
		print("Person")
	else:
		cv2.imwrite(database_folder + '/others/' + date + '_o.png',frame)
		command = ['cp', darknet_folder + 'predictions.png', database_folder + '/person/' + date + '.png']
		subprocess.run(command)
		print("Nothing")

	with open("log.log", "a") as myfile:
    		myfile.write(date + " - " + output)



	print("FINISHED - "+datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"))

if __name__ == '__main__':

	# initialize the first frame in the video stream
	firstFrame = None

	camera = cv2.VideoCapture(0)
	time.sleep(0.25)
	change = False

	wait = Process(target=time.sleep, args=(1,))
	wait.start()

	checking = Process(target=time.sleep, args=(1,))
	checking.start()

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
		(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
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

		# show the camera
		cv2.imshow("Camera", frame)
		cv2.imshow("Thresh", thresh)
		cv2.imshow("Frame Delta", frameDelta)
		key = cv2.waitKey(1) & 0xFF

		if (wait.exitcode != None and checking.exitcode != None):
			firstFrame = gray
			if (change):
				cv2.imwrite('img.png',frame)
				time.sleep(0.20)
				_frame = frame
				_date = date
				checking = Process(target=checkImage, args=(_frame, _date))
				checking.start()
				change = False
				print("CHANGE")
			else:		
				wait = Process(target=time.sleep, args=(5,))
				wait.start()
				print("NO CHANGE")

		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break

		
		time.sleep(min_delay)

	# cleanup the camera and close any open windows
	camera.release()
	cv2.destroyAllWindows()

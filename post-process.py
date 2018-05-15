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
input_folder = current_folder + "/input"
output_folder = current_folder + "/output"
darknet_folder = "/home/osboxes/darknet-master/"
darknet_config = "cfg/yolov3.cfg"
darknet_weights = "yolov3.weights"

def checkImage(frame, filename):
	name = datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
	print("START - "+datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"))
	command = ["./darknet", "detect", darknet_config, darknet_weights, input_folder + "/" + filename, "/dev/null"]
	p = subprocess.Popen(command, cwd=darknet_folder, stdout=subprocess.PIPE)
	p.wait()
	output = p.stdout.read().decode("utf-8")
	print("Output: "+output)
	
	# predictions
	pred = cv2.imread(darknet_folder + 'predictions.png')
	cv2.imshow("Predictions", pred)

	# cat
	if "cat" in output:
		command = ['cp', darknet_folder + 'predictions.png', database_folder + '/cat/' + name + ".png"]
		subprocess.run(command)
		print("cat")
	# dog
	elif "dog" in output:
		command = ['cp', darknet_folder + 'predictions.png', database_folder + '/dog/' + name + ".png"]
		subprocess.run(command)
		print("dog")
	# person
	elif "person" in output:
		command = ['cp', darknet_folder + 'predictions.png', database_folder + '/person/' + name + ".png"]
		subprocess.run(command)
		print("Person")
	else:
		command = ['cp', darknet_folder + 'predictions.png', database_folder + '/others/' + name + ".png"]
		subprocess.run(command)
		print("Nothing")

	#log
	with open("log.log", "a") as myfile:
    		myfile.write(name + " - " + output)

	print("FINISHED - "+datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"))

if __name__ == '__main__':
	for filename in os.listdir(input_folder):
		img = cv2.imread(filename)
		cv2.imshow("Picture", img)
		checkImage(img, filename)


import glob
import os
import sys
import select
import cv2
import pygame

import config
import face

#import buttons



# Prefix for positive training image filenames.
POSITIVE_FILE_PREFIX = 'positive_'



def capture():
	camera = config.get_camera()
	
	# Create the directory for positive training images if it doesn't exist.
	if not os.path.exists(config.POSITIVE_DIR):
		os.makedirs(config.POSITIVE_DIR)
	# Find the largest ID of existing positive images.
	# Start new images after this ID value.
	files = sorted(glob.glob(os.path.join(config.POSITIVE_DIR, 
		POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].pgm')))
	count = 0
	if len(files) > 0:
		# Grab the count from the last filename.
		count = int(files[-1][-7:-4])+1
	
	print 'Capturing image...'
	image = camera.read()
	# Convert image to grayscale
	image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	# Get coordinates of single face in captured image.
	result = face.detect_single(image)
	if result is None:
	    print 'Could not detect single face!  Check the image in capture.pgm' \
		      ' to see what was captured and try again with only one face visible.'
	    return False
	
	#if buttons.decideAdd_button():

        x, y, w, h = result
	# Crop image as close as possible to desired face aspect ratio.
	# Might be smaller if face is near edge of image.
	crop = face.crop(image, x, y, w, h)
       

	# Save image to file.
	filename = os.path.join(config.POSITIVE_DIR, POSITIVE_FILE_PREFIX + '%03d.pgm' % count)
	cv2.imwrite(filename, crop)
	print 'Found face and wrote training image', filename
	return True
	

def capture1():
        camera = config.get_camera()

        # Create the directory for positive training images if it doesn't exist.
        if not os.path.exists(config.POSITIVE_DIR1):
                os.makedirs(config.POSITIVE_DIR1)
        # Find the largest ID of existing positive images.
        # Start new images after this ID value.
        files = sorted(glob.glob(os.path.join(config.POSITIVE_DIR1,
                POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].pgm')))
        count = 0
        if len(files) > 0:
                # Grab the count from the last filename.
                count = int(files[-1][-7:-4])+1

        print 'Capturing image...'
        image = camera.read()
        # Convert image to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # Get coordinates of single face in captured image.
        result = face.detect_single(image)
        if result is None:
            print 'Could not detect single face!  Check the image in capture.pgm' \
                      ' to see what was captured and try again with only one face visible.'
            return False

        #if buttons.decideAdd_button():

        x, y, w, h = result
        # Crop image as close as possible to desired face aspect ratio.
        # Might be smaller if face is near edge of image.
        crop = face.crop(image, x, y, w, h)


        # Save image to file.
        filename = os.path.join(config.POSITIVE_DIR1, POSITIVE_FILE_PREFIX + '%03d.pgm' % count)
        cv2.imwrite(filename, crop)
        print 'Found face and wrote training image', filename
        return True



import train
import config
import face

import cv2
import os
camera = config.get_camera()

def load_data():
    train.train_classifier()
    train.train_classifier1()

    #Load training data into model
    print 'Loading training data...'
    model = cv2.createEigenFaceRecognizer()
    #Trianed classifier
    model.load(config.TRAINING_FILE)

    
    model1 = cv2.createEigenFaceRecognizer()
    model1.load(config.TRAINING_FILE1)

    print 'Training data loaded!'
    return model,model1

#if recognized, return true, otherwise return false
def classify(model,model1):
    print "predicting"
    image = camera.read()
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    result = face.detect_single(image)
    if result is None:
        print 'Could not detect single face!  Check the image in capture.pgm' \
		  ' to see what was captured and try again with only one face visible.'
        
        return False
    print "Single face detected"
    x, y, w, h = result
    crop = face.resize(face.crop(image, x, y, w, h))
    # Test face against model.
    label, confidence = model.predict(crop)
    label1, confidence1 = model1.predict(crop)
    
    print 'Predicted {0} face with confidence {1} (lower is more confident).'.format('POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE', confidence)
    print 'Predicted {0} face with confidence {1} (lower is more confident).'.format('POSITIVE' if label1 == config.POSITIVE_LABEL else 'NEGATIVE', confidence1)
    if (label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD) or  (label1 == config.POSITIVE_LABEL and confidence1 < config.POSITIVE_THRESHOLD) :
        print 'Recognized face!'
	'''TO DO'''
	return True
    else:
	print 'Did not recognize face!'
	'''TO DO'''
	return False

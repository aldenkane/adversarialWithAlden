# faceRecog_SVM.py
# A script to recognize faces uses Adam Geitgey's face_recognition() API
# Original source code from https://github.com/ageitgey/face_recognition/blob/master/examples/face_recognition_svm.py, modified by Alden Kane
# adversarialWithAlden, Alden Kane's adversarial facial recognition research, supervised by Dr. Patrick Flynn
# This script train multiple images per person, then finds and recognize faces in an image using a SVC with scikit-learn

"""
Structure:
        <test_image>.jpg
        <train_dir>/
            <person_1>/
                <person_1_face-1>.jpg
                <person_1_face-2>.jpg
                .
                .
                <person_1_face-n>.jpg
           <person_2>/
                <person_2_face-1>.jpg
                <person_2_face-2>.jpg
                .
                .
                <person_2_face-n>.jpg
            .
            .
            <person_n>/
                <person_n_face-1>.jpg
                <person_n_face-2>.jpg
                .
                .
                <person_n_face-n>.jpg
"""

import face_recognition
from sklearn import svm
import glob
import os

# Training the SVC classifier
train_Path = '/Users/aldenkane1/Documents/1College/adversarialWithAlden/dataSet/train_dir'
test_Path = '/Users/aldenkane1/Documents/1College/adversarialWithAlden/dataSet/test_dir'

# Function to ignore hidden directories
def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))

# The training data would be all the face encodings from all the known images and the labels are their names
encodings = []
names = []

# Training directory
train_dir = listdir_nohidden(train_Path)
test_dir = listdir_nohidden(test_Path)

# Loop through each person in the training directory
for person in train_dir:
    pix = listdir_nohidden(person)

    # Loop through each training image for the current person
    for person_img in pix:
        # Get the face encodings for the face in each image file
        face = face_recognition.load_image_file(person_img)
        face_bounding_boxes = face_recognition.face_locations(face)

        #If training image contains exactly one face
        if len(face_bounding_boxes) == 1:
            face_enc = face_recognition.face_encodings(face)[0]
            # Add face encoding for current image with corresponding label (name) to the training data
            encodings.append(face_enc)
            names.append(person)
        else:
            print(person_img + " was skipped and can't be used for training")

# Create and train the SVC classifier
clf = svm.SVC(gamma='scale')
clf.fit(encodings,names)

for person in test_dir:
    pix = listdir_nohidden(person)
    for test_img in pix:
        # Load the test image with unknown faces into a numpy array
        test_image = face_recognition.load_image_file(test_img)

        # Find all the faces in the test image using the default HOG-based model
        face_locations = face_recognition.face_locations(test_image)
        no = len(face_locations)
        print("Number of faces detected: ", no)

        # Predict all the faces in the test image using the trained classifier
        print("Found:")
        for i in range(no):
            test_image_enc = face_recognition.face_encodings(test_image)[i]
            name = clf.predict([test_image_enc])
            print(*name)
"""
A simple testing file for our OpenCV object (read: person) tracking implementation.

Given a folder in media, it will search for the "input" directory,
process all the individual frames of the video in order (numbered 1.ext, 2.ext,
... n.ext) and then compile a tracking video exported in to media/folder/output.

To run test on folder, add the folder with input/output subfolders into media folder, and check
exclusion.txt file to exclude the folders you do not want to test.

To change object tracker, go to line 80 in run-tests.py and change array number for tracker type.

In the future, a separate test script that reads from the camera should be implemented
to ensure robust unit tests.

Also need to add a way to define initial bounding box around object, whether it be manually
in ui or with object detection.

TODO Lines 110-117 140 and 166
"""

import cv2
import os
import sys
from PIL import Image
# Importing Pillow Python Imaging Library:that adds support for opening, manipulating, and saving many different image file formats.
from PIL.ExifTags import TAGS


def draw(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (0, 255, 255), 3, 1)


# General configurations
suffix = ""
media_path = "./media"
input_dirname = "input"
output_dirname = "output"
image_extension = ".jpg"

(major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')

directory_items = os.listdir(media_path)

# Extract all folders in media_path, unless they're in the exclusion.txt file
excluded_folders = [folder.strip() for folder in open(media_path + "/exclusion.txt").readlines()]

directory_folders = [item for item in directory_items
                     if os.path.isdir("{}/{}".format(media_path, item)) and item not in excluded_folders]

print("\n### Beginning OpenCV tests ###\n\n")

warning_count = 0

for item in directory_folders:
    # Try to find input directory
    if input_dirname not in os.listdir("{}/{}".format(media_path, item)):
        print("\n### WARNING ### on {} test: Failed to find input directory. Proceeding to next test. \n".format(item))
        warning_count += 1
        continue

    print("### Testing input from '{}/input...'".format(item))

    # Load frames.
    frames = [frame for frame in os.listdir("{}/{}/{}".format(media_path, item, input_dirname))]

    # Validate all file extensions.
    for frame in frames:
        if frame[len(image_extension) - 1:] != image_extension:
            print("### WARNING ### Some files in {}/input found  to be not of the supported type '{}'"
                  .format(item, image_extension))
            warning_count += 1
            break

    # Set up tracker.
    # Change array value in line 80 to change tracker.

    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[6]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.legacy.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

    # Read video frame by frame.
    # Read first frame.

    # Initialization of tracker and bbox
    frame = cv2.imread("{}/{}/{}/{}".format(media_path, item, input_dirname, frames[0]))



    # bbox = cv2.selectROI("output", frame, False)  # draw bounding box with OpenCV UI
    ###
    # TODO need JS UI to draw bounding box for tests
    ###

    # Define an initial bounding box
    # TODO: make this come from a config file in a test's folder
    bbox = (0, 0, 1000, 177)

    tracker.init(frame, bbox)

    success = True

    for index in range(1, len(frames)):
        frame_filepath = "{}/{}/{}/{}".format(media_path, item, input_dirname, frames[index])

        frame = cv2.imread(frame_filepath)

        success, bbox = tracker.update(frame)

        #Retrieve image GPS and datetime values.
        try:
            image = Image.open(frame_filepath)
            # raise an IOError if file cannot be found,or the image cannot be opened.
        except:
            IOError
            # dictionary to store metadata keys and value pairs.
        exif = {}

        # iterating over the dictionary 
        #TODO Change so only uses gps and doesn't iterate rest.
        for tag, value in image.getexif().items():
        #extarcting all the metadata as key and value pairs and converting them from numerical value to string values
            if tag in TAGS:
                exif[TAGS[tag]] = value

        if 'GPSInfo' in exif:
            gps = exif['GPSInfo']
        else:
            gps = "No GPS data found"

        if 'DateTime' in exif:
            datetime = exif['DateTime']
        else:
            datetime = "No datetime info found"

    
        if success:
            draw(frame, bbox)
        else:
            cv2.putText(frame, "LOST", (75, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)


        # Display tracker type on frame
        #TODO Absolute pixel values so frontend should calibrate where the information is on screen.
        cv2.putText(frame, tracker_type + " Tracker", (75, 980), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
        cv2.putText(frame, "Coordinates: " + gps, (75, 1020), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
        cv2.putText(frame, "Datetime: " + datetime, (75, 1060), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
        # write to frame name
        cv2.imwrite("{}/{}/{}/{}".format(media_path, item, output_dirname, frames[index]), frame)

if warning_count:
    print("### OpenCV tests completed with {} WARNINGs. ###".format(warning_count))
else:
    print("### OpenCV tests completed. Check outputs.")

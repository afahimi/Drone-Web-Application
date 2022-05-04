from pickle import TRUE
import cv2
import os
import sys
from PIL import Image
import time
# Importing Pillow Python Imaging Library:that adds support for opening, manipulating, and saving many different image file formats.


class Tracker(object):
    def __init__(self, payload_call_func):
        self.payload_call_func = payload_call_func
        self.track()

    # Output
    def send_command_to_payload(self, command):
        self.payload_call_func(None)

    # Input
    def setEnabled(self, enabled):
        print("setEnabled called with", enabled)

    # Input
    def updateBoundingBox(self, bb):
        print("updateBoundingBox called with", bb)

    def draw(self, img, bbox):
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(img, (x, y), ((x + w), (y + h)), (0, 255, 255), 3, 1)

    def track(self):
        # General configurations
        suffix = ""
        media_path = "./media"
        input_dirname = "input"
        output_dirname = "output"
        image_extension = ".jpg"

        (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')

        directory_items = os.listdir(media_path)

        # Extract all folders in media_path, unless they're in the exclusion.txt file
        excluded_folders = [folder.strip() for folder in open(
            media_path + "/exclusion.txt").readlines()]

        directory_folders = [item for item in directory_items
                             if os.path.isdir("{}/{}".format(media_path, item)) and item not in excluded_folders]

        print("\n### Stalker Starting ###\n\n")

        warning_count = 0

        for item in directory_folders:
            # Try to find input directory
            if input_dirname not in os.listdir("{}/{}".format(media_path, item)):
                print(
                    "\n### WARNING ### on {} test: Failed to find input directory. Proceeding to next test. \n".format(item))
                warning_count += 1
                continue

            print("### Testing input from '{}/input...'".format(item))

            # Load frames.
            frames = [frame for frame in os.listdir(
                "{}/{}/{}".format(media_path, item, input_dirname))]

            # Validate all file extensions.
            for frame in frames:
                if frame[len(image_extension) - 1:] != image_extension:
                    print("### WARNING ### Some files in {}/input found  to be not of the supported type '{}'"
                          .format(item, image_extension))
                    warning_count += 1
                    break

            # Set up tracker.
            # Change array value in line 80 to change tracker.

            tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD',
                             'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
            tracker_type = tracker_types[6]

            if int(minor_ver) < 3:
                tracker = cv2.Tracker_create(tracker_type)
            else:
                if tracker_type == 'BOOSTING':  # 0
                    tracker = cv2.TrackerBoosting_create()
                if tracker_type == 'MIL':  # 1
                    tracker = cv2.TrackerMIL_create()
                if tracker_type == 'KCF':  # 2
                    tracker = cv2.TrackerKCF_create()
                if tracker_type == 'TLD':  # 3
                    tracker = cv2.TrackerTLD_create()
                if tracker_type == 'MEDIANFLOW':  # 4
                    tracker = cv2.TrackerMedianFlow_create()
                if tracker_type == 'GOTURN':  # 5
                    tracker = cv2.TrackerGOTURN_create()
                if tracker_type == 'MOSSE':  # 6
                    tracker = cv2.legacy.TrackerMOSSE_create()
                if tracker_type == "CSRT":  # 7
                    tracker = cv2.TrackerCSRT_create()

            # Read video frame by frame.
            # Read first frame.

            # Initialization of tracker and bbox
            frame = cv2.imread(
                "{}/{}/{}/{}".format(media_path, item, input_dirname, frames[0]))

            imageSize = {frame.height, frame.width}

            tracker.init(frame, bbox)

            success = True
            index = 0

            # Iterate through images in media input folder
            while(frames[index]):
                frame_filepath = "{}/{}/{}/{}".format(
                    media_path, item, input_dirname, frames[index])

                frame = cv2.imread(frame_filepath)

                success, bbox = tracker.update(frame)

                # Display tracker type on frame
                cv2.putText(frame, tracker_type + " Tracker", (75, 980),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
                # write to frame name
                cv2.imwrite("{}/{}/{}/{}".format(media_path, item,
                            output_dirname, frames[index]), frame)

                # Find gimbal adjustments (5472 × 3648 image)
                bboxCentre = {(bbox[0]+(bbox[2]/2), bbox[1]+bbox[3]/2)}

                # Mapping pixels to -1 to 1
                horizontalCartesianShift = bboxCentre[0] * 2.0 / imageSize[0] - 1
                verticalCartesianShift = bboxCentre[1] * 2.0 / imageSize[1] - 1

                # Send gimbal shift to payload
                self.send_command_to_payload(
                    {"JoystickX": horizontalCartesianShift, "JoystickY": verticalCartesianShift})

                if frames[index+1] != success:
                    time.sleep(100)
                else:
                    index += 1

        if warning_count:
            print("### Tracking completed with {} WARNINGs. ###".format(
                warning_count))
        else:
            print("### Tracking completed. Check outputs.")

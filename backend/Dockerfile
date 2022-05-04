# Python runtime environment setup
FROM python:3.7
WORKDIR /home/stalker/backend

# Need this on the container prior to the volume mounting
COPY backend/requirements.txt /home/stalker/backend/requirements.txt

# Install OpenCV and Flask dependencies
RUN apt-get update && apt-get install -y \
    python3-opencv

# Install opencv-python, headless since we don't need the GUI features of the library
# as well as Flask and Flask dependencies
RUN pip install -r /home/stalker/backend/requirements.txt

# Persist image after main process has ended, for testing
CMD tail -f /dev/null

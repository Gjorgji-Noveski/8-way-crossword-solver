FROM debian
COPY the_program ./the_program
WORKDIR ./the_program
RUN adduser --quiet --disabled-password solver-user && chmod -R a+rw .
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-mkd python3-pyqt5 python3-pip
RUN pip install opencv-python-headless
CMD ["python3", "GUI.py"]

# and before that root should be added to list of xhost authorized clients like so: xhost +local:
# but if a user is added to the docker container, this is not necessary
# this needs to be called like so: sudo docker run --mount type=bind,source="$(pwd)"/data,target=/the_program/data --mount type=bind,source=/tmp/.X11-unix/,target=/tmp/.X11-unix/ -e DISPLAY=$DISPLAY -u solver-user <CONTAINER_ID>
FROM debian
COPY the_program ./the_program
WORKDIR ./the_program
RUN export QT_DEBUG_PLUGINS=1 && apt-get update && apt-get install -y libxcb-xinerama0 ffmpeg libsm6 libxext6 tesseract-ocr tesseract-ocr-mkd python3-pyqt5 python3-pip
RUN pip install opencv-python-headless
CMD ["python3", "GUI.py"]

# this needs to be called like so: sudo docker run -it -v /tmp/.X11-unix/:/tmp/.X11-unix -e DISPLAY=$DISPLAY <CONTAINER_ID>
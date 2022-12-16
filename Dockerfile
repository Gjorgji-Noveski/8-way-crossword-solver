FROM debian
COPY the_program ./the_program
COPY data ./the_program/data/
WORKDIR ./the_program
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-mkd python3-pyqt5 python3-pip
RUN pip install opencv-python-headless
CMD ["python3", "GUI.py"]

# this needs to be called like so: sudo docker run -it -v /tmp/.X11-unix/:/tmp/.X11-unix -e DISPLAY=$DISPLAY <CONTAINER_ID>
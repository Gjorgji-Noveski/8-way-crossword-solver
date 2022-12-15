FROM python:3.8
COPY the_program ./the_program
WORKDIR ./the_program
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 tesseract-ocr tesseract-ocr-mkd python3-pip
RUN pip install PyQt5
CMD ["python", "GUI.py"]

FROM alpine
COPY the_program .
WORKDIR ./the_program
RUN apk add py3-pip
RUN pip install -r requirements.txt
RUN python GUI.py
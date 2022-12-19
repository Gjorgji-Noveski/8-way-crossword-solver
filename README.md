# Crossword Solver

Crossword Solver is a program that locates solutions for 8-way crosswords.
The 8-way crosswords are different from the typical crosswords we might think of.
Instead of filling in words, in this crossword letters are already filled out in a grid.
We are given a set of pictures, and we try to find the words that represent the picture.
The words can be in 8 different orientations in the word grid:
- from left to right
- from top-left to bottom-right
- from top to bottom
- from top-right to bottom left, and so on

![Example image of an eight way crossword](./example-8-way-crossword.png)

The crossword solver is a tool in which you can input a picture of an 8-way crossword, 
give it some words to search, and it will find where those words are located in the word grid.

-------------------
This repository contains the image for running the 8-way-crossword-solver application.
An 8-way crossword is a crossword which already has letters filled out in every grid cell. The task is to find given words in the grid which may appear in 8 different directions. 

## Running on Linux
In order to run this image, firstly you have to pull it from the repository:

`docker pull gjorgjin/8-way-crossword-solver`

After pulling the image, run it with the following docker command:

`docker run --mount type=bind,source="$(pwd)"/data,target=/the_program/data --mount type=bind,source=/tmp/.X11-unix/,target=/tmp/.X11-unix/ -e DISPLAY=$DISPLAY <CONTAINER_ID>`

With this command we connect(bind) several folders from the host machine to the docker container.
One bind is for allowing the user to upload images to the folder which will be reflected into the running container application. 
The other bind is for exposing the X server socket from the user's host machine to the docker container in order for the program to be displayed.
And the last parameter is setting up the environment variable to tell the program on which display it should connect to.


If you are getting permission denied for these commands, add `sudo` before each command call.
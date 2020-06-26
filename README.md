# youtube-download-server

Simple server that enables an API for clients to call to get a youtube video sent as mp4 file. \
Server downloads and stores the mp4 videos. The same video will be sent upon concurrent request for a video.\
Videos are stored in the server up till one month after their creation, then they will be deleted. This one month duration can be adjusted as argument to application.

## Installation

Needs python libraries "schedule" and "youtube_dl" to be installed. \
Must use python 3 as server package only works in python 3.\
Has only been tested using Python 3.8 on Ubuntu 20.04.

All steps in case nothing is installed:

> sudo apt update

> sudo apt install python3

> sudo apt install python3-pip

> sudo pip3 install youtube_dl

> sudo pip3 install schedule

Unpackage the python files where you want the server to be deployed.

## Starting the server

For options run:
> python3 youtube_download_server.py -h

Running server with default settings(deletion after 30 days, and port 8000):
> python3 youtube_download_server.py

Once server started, the API address will look something like this:
> 192.168.0.127:8000/getVideo?id=[YOUTUBE ID]

Server will download and send the requested file as a mp4 file.

## Maintenance
Once the server is up and running all videos will be stored in the subfolder "videos/", this folder gets created automatically in linux.\
All files are stored there with this syntax: "[date] [youtube id] [youtube name].mp4"

## Closing the server
After the program has been terminated either close the terminal or the remaining threads, as the schedueler thread might still be running in background.

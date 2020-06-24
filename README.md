# youtube-download-server

Simple server that enables an API for clients to call to get a downloaded video from server. 
Server saves and serves same videos upon concurrent request for same video.
Upon a certain duration all videos are deleeted, default set to 30 days. Can be adjusted as argument to youtube_download_server.

Needs "schedule" and "youtube_dl" to be installed. Must use python 3 as server only works in python 3.

Has only been tested on Ubuntu 20.04.

Run "python3 youtube_download_server.py -h" for options
For default settings(deletion after 30 days, and port 8000) just run "python3 youtube_download_server.py"

Once server started, API is called on something like:
192.168.0.127:8000/getVideo?id=[YOUTUBE ID]

After the program has been terminated either close the terminal or the remaining threads, as the schedueler thread might still be running in background.
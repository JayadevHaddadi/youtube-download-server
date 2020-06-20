# youtube-download-server

Simple server that enables an API for clients to call to get a downloaded video from server. 
Server saves and serves same videos upon concurrent request for same video.
Upon a certain duration all videos are deleeted.

Needs schedule and youtube_dl to be installed

One issue is after main process is killed the scheduler continues to run. That process needs to be killed manually.

#For youtube download
from __future__ import unicode_literals
import youtube_dl

# For server
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

#for files
from urllib import parse
import sys, os

#TumeStamp
import time;
from datetime import datetime

#deleting old files
import schedual_deletion

#arguments
import argparse

#for my ip
import socket

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        if parsed_path.path == '/getVideo':
            now = datetime.now()
            print("\n\n-----------",now.strftime("%Y-%m-%d %H:%M:%S"),"New request from",self.client_address[0])
            try:
                youtudeId = parsed_path.query.split("=")[1]
                full_path = 'https://www.youtube.com/watch?v=' + youtudeId

                ts = time.time()
                # timeObj = time.localtime(ts)
                dateTimeObj = datetime.now()
                timestampStr = dateTimeObj.strftime("%Y-%m-%d")
                # video_title = "%d-%d-%d" % (timeObj.tm_year,timeObj.tm_mon, timeObj.tm_mday)
                video_title = timestampStr
                ydl_opts = {}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(full_path, download=False)
                    youtube_title = info_dict.get('title', None)
                    youtube_title = ''.join(e for e in youtube_title if (e.isalnum() and e.isascii()) or e ==' ' or e =='-' )
                    youtube_title = youtube_title.replace("\\","")
                    youtube_title = youtube_title.replace("/","")
                    video_title += " " + youtudeId + " " + youtube_title.strip()

                fileName = 'videos/'+video_title+'.mp4'
                print("filename",fileName)
                ydl_opts = {'outtmpl': fileName}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(full_path, download=True)
                    # print("\nDownloaded:",video_title)
                    # print("Youtube ID:",youtudeId)

                with open(fileName, 'rb') as file:
                    self.send_response(200)
                    self.send_header("Content-Type", 'application/octet-stream')
                    self.send_header("Content-Disposition",
                        'attachment; filename="{}"'.format(fileName))
                    fs = os.fstat(file.fileno())
                    self.send_header("Content-Length", str(fs.st_size))
                    self.end_headers()
                    self.wfile.write(file.read())
                    print("----",fileName,"File successfully sent!\n")

            except BrokenPipeError as e:
                print("Client cancelled request for",youtudeId)
            except Exception as e:
                print("\n----- BEGIN EXCEPTION ------")
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(e)
                print("------ END EXCEPTION ------")

        else:
            print("Wrong api call",parsed_path.path)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Youtube download server with automatic download of old files')
    parser.add_argument('-port', type=int, default=8000, help="Port number for server")
    parser.add_argument('-days', type=int, default=30, help="Max age of downloaded files before they get deleted")
    args = parser.parse_args()
    PORT = args.port
    assert PORT > 1023 and PORT < 65535, "Port must be in range 1024-65534"
    DAYS = args.days

    schedual_deletion.start_job(DAYS)
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    server = ThreadedHTTPServer(('', PORT), GetHandler)
    print('Server started on port', PORT)
    print('For download call:')
    print(str(IPAddr)+":"+str(PORT)+"/getVideo?id=[YOUTUBE ID]")
    print('Use <Ctrl-C> to stop.')
    server.serve_forever()

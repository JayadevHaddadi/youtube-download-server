#For youtube download
from __future__ import unicode_literals 
import youtube_dl

# For server
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

#for files
from urllib import parse
import sys, os

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        fileName = 'failed'
        if parsed_path.path == '/getVideo':
            print("\nNew request:")
            try:    
                youtudeId = parsed_path.query.split("=")[1]
                full_path = 'https://www.youtube.com/watch?v=' + youtudeId

                fileName = 'videos/'+youtudeId+'.mp4'
                ydl_opts = {'outtmpl': fileName}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(full_path, download=True)
                    video_id = info_dict.get("id", None)
                    video_title = info_dict.get('title', None)
                    video_title = ''.join(e for e in video_title if e.isascii()) + ".mp4"
                    print("\nDownloaded:",video_title)
                    print("Youtube ID:",video_id)

                with open(fileName, 'rb') as file: 
                    self.send_response(200)
                    self.send_header("Content-Type", 'application/octet-stream')
                    self.send_header("Content-Disposition",
                        'attachment; filename="{}"'.format(video_title))
                    fs = os.fstat(file.fileno())
                    self.send_header("Content-Length", str(fs.st_size))
                    self.end_headers()
                    self.wfile.write(file.read()) 
                    print("File successfully sent!")

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

PORT = 8000
if __name__ == '__main__':
    server = ThreadedHTTPServer(('', PORT), GetHandler)
    print('Server started on port', PORT)
    print('Use <Ctrl-C> to stop.')
    server.serve_forever()
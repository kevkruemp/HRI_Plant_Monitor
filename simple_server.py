import SimpleHTTPServer
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import urlparse

port = 8000

class funHandler(BaseHTTPRequestHandler):
    # def do_GET(self, function, *args, **kwargs):
    def do_GET(self):
        print self.path
        self.send_response(200)
        return self.path

# httpd = SocketServer.TCPServer(("", port), MyHandler)
# httpd.serve_forever()
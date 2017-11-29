# server stuff
# import simple_server as simpleSrvr
from simple_server import *
# motor control stuff
import motor_control as motorCtrl

# firebase
from firebase import firebase
fb = firebase.FirebaseApplication('https://gal-9000.firebaseio.com/', None)

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
        if (self.path == '/up'):
            motor_move(-1000)
            fb_put('up')
        elif (self.path =='/down'):
            motor_move(1000)
            fb_put('down')
        elif (self.path == '/stop'):
            motor_move(0)
        return self.path

def fb_put(state):
    fb.put('gal-9000','blinds',state)

def check_motor_pos():
    load = motorCtrl.get_load(1)[0]
    if (load == -100):
        return 'down'
    elif (load == 100):
        return 'up'
    else:
        return 'mid'

def motor_move(speed):
    motorCtrl.move_wheel(1, speed)

if __name__ == "__main__":

    motorHandler = funHandler
    # motorHandler.do_GET = motor_get
    # motorHandler.do_GET = motorHandler.do_GET(simpleSrvr.funHandler, motor_get)
    # motorHandler.do_GET = motor_get

    httpd = SocketServer.TCPServer(("", port), motorHandler)
    httpd.serve_forever()
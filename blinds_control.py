# server stuff
# import simple_server as simpleSrvr
from simple_server import *
# motor control stuff
import motor_control as motorCtrl

# GPIO setup
import RPi.GPIO as GPIO
# use gpio pin 4 (pin 7)
gpio_in = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_in,GPIO.IN)

# firebase
from firebase import firebase
fb = firebase.FirebaseApplication('https://gal-9000.firebaseio.com/', None)

blossom_add = 'http://10.148.9.99:5555/s/'
blinds_state = ''

# sending http requests
import urllib2

# threading
import threading

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
        move_blinds(self.path[1:])

def fb_thread():
    if (GPIO.input(gpio_in)):
        blinds_state = fb_check()

def fb_put(state):
    fb.put('blinds','state',state)

def fb_check():
    blinds_cmd = fb.get('blinds','cmd')
    blinds_state = fb.get('blinds','state')
    blossom_s = fb.get('blossom','s')
    blossom_idle = fb.get('blossom','idle')

    move_blinds(blinds_cmd)

    # command blossom
    urllib2.urlopen(blossom_add+blossom_s+'/'+blossom_idle)

    return blinds_state


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

def move_blinds(state):
    if (state == 'up'):
        motor_move(-1000)
        # fb_put('up')
    elif (state =='down'):
        motor_move(1000)
        # fb_put('down')
    elif (state == 'stop'):
        motor_move(0)
    fb.put('blinds','state',state)


if __name__ == "__main__":
    blinds_state = fb_check()
    t = threading.Thread(target=fb_thread)
    t.start()
    motorHandler = funHandler
    # motorHandler.do_GET = motor_get
    # motorHandler.do_GET = motorHandler.do_GET(simpleSrvr.funHandler, motor_get)
    # motorHandler.do_GET = motor_get

    httpd = SocketServer.TCPServer(("", port), motorHandler)
    httpd.serve_forever()
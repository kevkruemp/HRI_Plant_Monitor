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

blossom_add = 'http://10.156.9.99:5555/s/'
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

# firebase functions
def fb_thread():
    while(1):
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
    blossom_cmd = blossom_add+blossom_s+'/'+blossom_idle
    try:
        urllib2.urlopen(blossom_cmd)
        print blossom_cmd
    except:
        pass

    # erase commands
    fb.put('blinds','cmd','')

    return blinds_state

# motor functions
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
    else:
        return
    fb.put('blinds','state',state)

# main
if __name__ == "__main__":

    # set function handler
    motorHandler = funHandler

    # init blinds state
    blinds_state = fb_check()

    # start threading
    t = threading.Thread(target=fb_thread)
    t.start()

    httpd = SocketServer.TCPServer(("", port), motorHandler)
    httpd.serve_forever()
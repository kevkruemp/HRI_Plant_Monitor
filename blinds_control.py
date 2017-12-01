# server stuff
# import simple_server as simpleSrvr
from simple_server import *
# motor control stuff
import motor_control as motorCtrl

# GPIO setup
import RPi.GPIO as GPIO
# GPIO 4 (pin 7) goes up
gpio_up = 4
# GPIO 3 (pin 5) goes down
gpio_down = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_up,GPIO.IN)
GPIO.setup(gpio_down,GPIO.IN)

# firebase
from firebase import firebase
fb = firebase.FirebaseApplication('https://gal-9000.firebaseio.com/', None)

blossom_add = 'http://10.156.9.99:5555/s/'
blinds_state = ''
blossom_blinds = {'up':'fear2','down':'sad3'}

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
        try:
            if (GPIO.input(gpio_up)):
                move_blinds('up')
            elif (GPIO.input(gpio_down)):
                move_blinds('down')
        except KeyboardInterrupt:
            return

def fb_put(state):
    fb.put('blinds','state',state)

def fb_check():
    blinds_cmd = fb.get('blinds','cmd')
    blinds_state = fb.get('blinds','state')
    blossom_s = fb.get('blossom','s')
    blossom_idle = fb.get('blossom','idle')

    cmd_blossom(blossom_s, blossom_idle)

    # move blinds
    move_blinds(blinds_cmd)
    # erase commands
    fb.put('blinds','cmd','')

    return blinds_state

def cmd_blossom(blossom_s, blossom_idle):
    # command blossom
    blossom_cmd = blossom_add+blossom_s+'/'+blossom_idle
    print blossom_cmd
    try:
        urllib2.urlopen(blossom_cmd)
    except:
        pass

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
        return
    else:
        return
    fb.put('blinds','state',state)
    cmd_blossom(blossom_blinds[state],'')

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
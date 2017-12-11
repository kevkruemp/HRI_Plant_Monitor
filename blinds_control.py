# server stuff
# import simple_server as simpleSrvr
from simple_server import *
# motor control stuff
import motor_control as motorCtrl

# blossom control
import blossom_control as blossom
# blossom info
blossom_add = blossom.blossom_add
blossom_blinds = {'raise':'fear2','lower':'sad3','':'yes'}

# GPIO setup
import RPi.GPIO as GPIO
# GPIO 4 (pin 7) goes up
gpio_up = 4
# GPIO 3 (pin 5) goes down
gpio_down = 3
# GPIO 2 (pin 3) commands blossom
gpio_blossom = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_up,GPIO.IN)
GPIO.setup(gpio_down,GPIO.IN)
GPIO.setup(gpio_blossom,GPIO.IN)

import firebase_control
from firebase_control import fb as gal9000

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

# poll gal9000 firebase
def gal9000_thread():
    while(1):
        try:
            if (GPIO.input(gpio_up)):
                print 'Raising'
                move_blinds('raise')
            elif (GPIO.input(gpio_down)):
                print 'Lowering'
                move_blinds('lower')
            elif (GPIO.input(gpio_blossom)):
                print 'Blossoming'
                blossom.cmd_blossom('yes','calm')
        except KeyboardInterrupt:
            return

# poll blind position
def blind_pos_thread():
    while(1):
        try:
            motor_load = motorCtrl.get_load(1)
            print motor_load
            blind_state = ''
            if (motor_load == 96.5):
                blind_state = 'up'
            elif(motor_load == -96.5):
                blind_state = 'down'
            if (blind_state != ''):
                gal9000.put('blinds','state',blind_state)
                print blind_state
        except KeyboardInterrupt:
            return

# check and update from firebase
def gal9000_check():
    blinds_cmd = gal9000.get('blinds','cmd')
    blinds_state = gal9000.get('blinds','state')
    blossom_s = gal9000.get('blossom','s')
    blossom_idle = gal9000.get('blossom','idle')

    # command blossom
    blossom.cmd_blossom(blossom_s, blossom_idle)

    # move blinds
    move_blinds(blinds_cmd)
    # erase commands
    gal9000.put('blinds','cmd','')

    return blinds_state

# move blinds 
def move_blinds(cmd):
    blossom.cmd_blossom(blossom_blinds[cmd])
    blinds_state = ''
    if (cmd == 'raise'):
        motorCtrl.move_to_limit(1,-1000)
        blinds_state = 'up'
        # gal9000_put('up')
    elif (cmd =='lower'):
        motorCtrl.move_to_limit(1,1000)
        blinds_state = 'down'
        # gal9000_put('down')
    elif (cmd == 'stop'):
        motorCtrl.move_to_limit(1,0)
        return
    else:
        return
    gal9000.put('blinds','state',blinds_state)

# main
if __name__ == "__main__":

    try:
        # set function handler for http requests
        motorHandler = funHandler

        # init blinds state
        # blinds_state = gal9000_check()

        # start threading
        t = threading.Thread(target=gal9000_thread)
        t.start()
        # c = threading.Thread(target=blind_pos_thread)
        # c.start()

        # start server
        httpd = SocketServer.TCPServer(("", port), motorHandler)
        httpd.serve_forever()

    # catch ctrl-c
    except KeyboardInterrupt:
        httpd.shutdown()
        pass
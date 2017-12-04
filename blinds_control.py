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
gpio_blossom = 2
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

# firebase functions
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

def blind_pos_thread():
    while(1):
        try:
            motor_load = motorCtrl.get_load(1)
            blind_state = ''
            if (motor_load == -100):
                blind_state = 'up'
            elif(motor_load == 100):
                blind_state = 'down'
            if (blind_state != ''):
                gal9000.put('blinds','state',blind_state)
                print blind_state
        except KeyboardInterrupt:
            return


# def gal9000_put(state):
    # gal9000.put('blinds','state',state)

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

# motor functions
# def check_motor_pos():
#     load = motorCtrl.get_load(1)[0]
#     if (load == -100):
#         return 'down'
#     elif (load == 100):
#         return 'up'
#     else:
#         return 'mid'

def motor_move(speed):
    motorCtrl.move_wheel(1, speed)

def move_blinds(cmd):
    blossom.cmd_blossom(blossom_blinds[cmd])
    blinds_state = ''
    if (cmd == 'raise'):
        motor_move(-1000)
        # blinds_state = 'up'
        # gal9000_put('up')
    elif (cmd =='lower'):
        motor_move(1000)
        # blinds_state = 'down'
        # gal9000_put('down')
    elif (cmd == 'stop'):
        motor_move(0)
        return
    else:
        return
    # gal9000.put('blinds','state',blinds_state)

# main
if __name__ == "__main__":

    try:
        # set function handler
        motorHandler = funHandler

        motorCtrl.motors.set_torque_limit({1:100})

        # init blinds state
        # blinds_state = gal9000_check()

        # start threading
        t = threading.Thread(target=gal9000_thread)
        t.start()
        c = threading.Thread(target=blind_pos_thread)
        c.start()

        httpd = SocketServer.TCPServer(("", port), motorHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        pass
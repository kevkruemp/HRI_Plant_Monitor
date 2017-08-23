# time and threading for "interrupts" without blocking
import time, threading
# wiringpi for RPi GPIO control
import wiringpi
# adafruit_io for storing/receiving data
from Adafruit_IO import Client

# connect to adafruit_io
aio = Client('5f9b8952f573d34cb47c16df8a628c8d1bfca9a0')

# set up wiringpi
wiringpi.wiringPiSetupGpio()
# setup pin 18 
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)
delay_period = 0.01
# write default position
wiringpi.pwmWrite(18, 152)

# checking function
# periodically checks adafruit_io for the value in the feed
def checkIO():
	# receive and print the value in the Alexa feed
    print aio.receive('Alexa')
    # check if value is 'Rice'
    # if so then flip motor
    if (aio.receive('Alexa').value == 'Rice'):
        aio.send('Alexa', 'Testing')
        wiringpi.pwmWrite(18, 135)
        time.sleep(1)
        wiringpi.pwmWrite(18, 152)
    threading.Timer(1, checkIO).start()

checkIO()
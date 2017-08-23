import time, threading
import wiringpi
from Adafruit_IO import Client
aio = Client('5f9b8952f573d34cb47c16df8a628c8d1bfca9a0')
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)
delay_period = 0.01
wiringpi.pwmWrite(18, 152)
def checkIO():
    print aio.receive('Alexa')
    if (aio.receive('Alexa').value == 'Rice'):
        aio.send('Alexa', 'Testing')
        wiringpi.pwmWrite(18, 135)
        time.sleep(1)
        wiringpi.pwmWrite(18, 152)
    threading.Timer(1, checkIO).start()

checkIO()
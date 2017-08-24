import re
import time
import json
import RPi.GPIO as GPIO
from slackclient import SlackClient
''' This is the main controller of the plant monitor and contains the monitoring loop

'''

# GPIO Pin setup
pumpPin = 11
valve1Pin = 12
valve2Pin = 13
valve3Pin = 15
valve4Pin = 16
valve5Pin = 18
valve6Pin = 22
moisturePin = 19

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pumpPin, GPIO.OUT)
GPIO.setup(valve1Pin, GPIO.OUT)
GPIO.setup(valve2Pin, GPIO.OUT)
GPIO.setup(valve3Pin, GPIO.OUT)
GPIO.setup(valve4Pin, GPIO.OUT)
GPIO.setup(valve5Pin, GPIO.OUT)
GPIO.setup(valve6Pin, GPIO.OUT)
GPIO.setup(moisturePin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Name of the slack bot
botname = "alexabot"
# slack client ID for the testbot
slack_client = SlackClient("xoxb-230232365618-N2Ce1y2U47xi0pnHZXm8iBjF")

''' Interactions:
	Alexa, what is your water level?
	- My resevior is at __%

	The system detects a resevoir below 10%
	- slack in general: Resevoir is low, please refill me
		- flips boolean so it only alerts once
		- unflips boolean once water level is above 50%

	ALexa, when were the plants last watered?
	- respond: Last watered on [date, time]
'''

# find the user ID of the testbot
user_list = slack_client.api_call("users.list")
for user in user_list.get('members'):
	if user.get('name') == "testbot":
		slack_user_id = user.get('id')
		break
# connect the slack bot to slack
if slack_client.rtm_connect():
	print "connected!"


while True:
	for message in slack_client.rtm_read():
		# If a slack message is detected, see if it starts with a testbot callout
		if 'text' in message and message['text'].startswith("<@%s" % slack_user_id):
			print "message received: %s" % json.dumps(message, indent=2)

			message_text = message['text'].\
				split("<@%s" % slack_user_id)[1].\
				strip()
			# remove the testbot name form the message so it can be read
				
			# match the message content to key phrases to determine actions to be taken
			if re.match(r'.*(makerbot).*', message_text, re.IGNORECASE):
				slack_client.api_call("chat.postMessage", channel=message['channel'],
					text="It is always broken.",
					as_user=True)

	
	time.sleep(1)
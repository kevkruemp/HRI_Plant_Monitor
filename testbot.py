import re
import time
import json
from slackclient import SlackClient

# slack client ID for the testbot
slack_client = SlackClient("xoxb-230232365618-N2Ce1y2U47xi0pnHZXm8iBjF")

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

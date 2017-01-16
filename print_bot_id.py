import os
import sys

from slackclient import SlackClient

BOT_NAME = 'shiny-octo-pancake'
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def list_users():
	api_call = slack_client.api_call("users.list")
	if api_call.get("ok"):
		
		# retrieve all users so we can find bot
		users = api_call.get('members')

		# print users[0]
		for user in users:
			name = u'name'
			if name in user and user.get('name') == BOT_NAME:
				print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
	else:
		print("could not find bot user with the name " + BOT_NAME)

def main():
	list_users()
	return 0

if __name__ == '__main__':
	sys.exit(main())
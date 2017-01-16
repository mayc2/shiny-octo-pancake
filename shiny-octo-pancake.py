import os
import time
import sys
import rauth

"""

	SLACK API HANDLER

"""

from slackclient import SlackClient

#get bot id from env
BOT_ID = os.environ.get("BOT_ID")

#constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

#instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))

def handle_command(command, channel):
	"""
		Receives commands directed at the bot and determines if they
		are valid commands. If so, then acts on the commands. If not,
		returns back what it needs for clarification.
	"""
	def handle_help():
		commands = ["help","\nlist categories","\npoll [i.e. Thai, Mexican, American]","\nyelp [search params]"]
		return ", ".join(commands)

	def handle_list(command):
		
		def categories():
			categories = ["Restaurants","\nSandwiches","\nNightlife","\nBars","\nFood","\nAmerican (New)","\nItalian","\nAmerican (Traditional)","\nPizza","\nChinese","\nBreakfast & Brunch","\nFast Food","\nCoffee & Tea","\nSalad","\nCafes","\nBurgers","\nSeafood","\nJapanese","\nMexican","\nDelis","\nSushi Bars","\nAsian Fusion","\nMediterranean","\nFood Trucks","\nBakeries","\nMiddle Eastern","\nFood Stands","\nPubs","\nThai"]
			return ', '.join(categories)
		
		command = command.split()
		print(command)
		if len(command) == 2:
			if command[1] == "categories":
				return categories()
		else:
			return "Fail"

	def handle_lunch(command):
		units = [ "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen","sixteen", "seventeen", "eighteen", "nineteen",]
		tens = ["", "", "twenty", "thirty", "forty", "fifty"]
		def text2int(item, numwords={}):
			if not numwords:	
				numwords["and"] = (1, 0)
	    		for idx, word in enumerate(units):
	    			numwords[word] = (1, idx)
				for idx, word in enumerate(tens):     
					numwords[word] = (1, idx * 10)
				current = result = 0
				
				if item not in numwords:
					raise Exception("Illegal word: " + item)
				
				scale, increment = numwords[item]
				if increment < 20:
					increment+=1
				current = current * scale + increment 
			return current

		from itertools import imap

		command = command.lower().split(" at ")
		if command < 2:
			return "Lunch is coming! Add more details (i.e. lunch at [time, [place]])"

		for item in command:
			if any(i in item for i in units):
				item = item.split()
				if len(item) > 1:
					result = ""
					for i in range(len(item)):
						if i == 0:
							result = str(text2int(item[i])) + ":"
						else:
							result += str(text2int(item[i]))
				else:
					result = str(text2int(item[0])) + ":00"
			elif any(imap(lambda c:c.isdigit(),item)):
				result = item

		return result

	#Main Command Handler
	if command == "help" or command == "h":
		response = handle_help()
	elif command.startswith("list"):
		response = handle_list(command)
	elif command == "yelp":
		params = get_search_parameters(37.697666,-121.923204)
		response = get_results(params)
	elif command.startswith("lunch"):
		response = handle_lunch(command)
	else:
		print(command)
		response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
				"* command with numbers, delimited by spaces."
	

	slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)



def parse_slack_output(slack_rtm_output):
	"""
		The Slack Real Time Messaging API is an events firehose.
		this parsing function returns None unless a message is
		directed at the Bot, based on its ID.
	"""
	output_list = slack_rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			if output and 'text' in output and AT_BOT in output['text']:
				# return text after the @ mention, whitespace removed
				return output['text'].split(AT_BOT)[1].strip().lower(), \
						output['channel']
	return None, None



"""

	YELP API HANDLER
   
"""

# lat = 37.697666, long = -121.923204
def get_search_parameters(lat,long):
	params = {}
	params["term"] = "restaurants"
	params["ll"] = "{},{}".format(str(lat),str(long))
	params["radius_filter"] ="9656.06"
	params["limit"]= "20"
	params["locale"] = "en-US"
	params["open_now"] = True
	# params["open_at"] = str(open_at)
	return params

def get_token(client_id,client_secret):
	import requests
	import json

	data = {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret}
	r = requests.post("https://api.yelp.com/oauth2/token", data=data)
	data_map = json.loads(r.text)
	return data_map['token_type'], data_map['access_token']
	
def get_results(params):

	consumer_key = "6FrOHXBf9sz7aM21TDkOeA"
	consumer_secret = "KvYtMWGPninQULxRF5E1OuaugjNUmdA3rBeGUQyBXb4gptXhuKehJrB1qEqnArTJ"
	
	service = rauth.OAuth1Service(consumer_key = consumer_key, consumer_secret = consumer_secret, request_token_url = "https://api.yelp.com/oauth2/token", base_url = "http://api.yelp.com/v2/")
	token, token_secret = service.get_request_token()
	print(token,token_secret)

	request = session.get("http://api.yelp.com/v2/search",params=params)
	data = request.json()
	session.close()

	return data

"""

	MAIN SCRIPT

"""

def main():

	READ_WEBSOCKET_DELAY = 1 #1 second delay between reading from firehose
	if slack_client.rtm_connect():
		print("shiny-octo-pancake connected and running.")
		while True:
			command, channel = parse_slack_output(slack_client.rtm_read())
			print(command,channel)
			if command and channel:
				handle_command(command,channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token or bot ID?")
		return 1

	return 0

if __name__ == '__main__':
	sys.exit(main())
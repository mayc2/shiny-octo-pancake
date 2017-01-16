import requests
import json
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError

lat = 37.697666 
lon = -121.923204
parameters = {}
parameters["term"] = "restaurants"
parameters["latitude"] = str(lat)
parameters["longitude"] = str(lon)
parameters["radius_filter"] = "9656.06"
parameters["limit"]= "20"
parameters["locale"] = "en-US"


data = {"grant_type": "client_credentials", "client_id": "6FrOHXBf9sz7aM21TDkOeA", "client_secret": "KvYtMWGPninQULxRF5E1OuaugjNUmdA3rBeGUQyBXb4gptXhuKehJrB1qEqnArTJ"}
r = requests.post("https://api.yelp.com/oauth2/token", data=data)
# r
# print(r.text)
token = r.json()

# print(data_map)
# print(data_map['access_token'])

consumer_key = "6FrOHXBf9sz7aM21TDkOeA"
consumer_secret = "KvYtMWGPninQULxRF5E1OuaugjNUmdA3rBeGUQyBXb4gptXhuKehJrB1qEqnArTJ"
protected_url = "https://api.yelp.com/v3/businesses/search"
refresh_url = "https://api.yelp.com/oauth2/token"
extra = {
	'client_id': consumer_key,
	'client_secret': consumer_secret,
}
# request_token = data_map['']
# request_token_secret = data_map['']
# session = OAuth1Session(consumer_key, consumer_secret, data_map['access_token'], data_map['access_token'])
# response = session.get("https://api.yelp.com/v3/businesses/search",parameters=parameters)
# # print(token.text)
# response_json = response.json()
# print(response_json)
headers = {}
headers['Authorization'] = "bearer" + token['access_token']
headers['Content-Type'] = "application/x-www-form-urlencoded"
# print(parameters)

client = OAuth2Session(consumer_key, token=token, auto_refresh_url=refresh_url, auto_refresh_kwargs=extra)
response = client.request("GET", protected_url, headers=headers, params=parameters)
print(response.text)


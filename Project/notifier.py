import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import json
import tweepy
import requests
import time




# SMS API Config
postUrl='http://panel.vatansms.com/panel/smsgonder1Npost.php'
musteriNo='39944'
kullaniciAdi='905350274019'
sifre='190wud40'
orjinator="MHMD.OKUMUS"

tur='Normal' """ Normal yada Turkce """
zaman=''

def send_SMS(sender, text, phone):
	mesaj=sender + ": " + text
	numara=phone

	string = """
	<sms>
		<kno>"""+musteriNo+"""</kno>
		<kulad>"""+kullaniciAdi+"""</kulad>
		<sifre>"""+sifre+"""</sifre>
		<gonderen>"""+orjinator+"""</gonderen>
		<mesaj>"""+mesaj+"""</mesaj>
		<numaralar>"""+phone+"""</numaralar>
		<tur>"""+tur+"""</tur>
	</sms>
	"""

	response =  requests.post(postUrl, data={"data":string})
	print(response.text)		

# Twitter Config
# Variables that contains the credentials to access Twitter API
ACCESS_TOKEN = '3317234002-pkNlyFMghEXwkkE9ohdvLsgWLzHn9wMV5QJouoQ'
ACCESS_SECRET = '6PKsu6SL15MSpsej26TnXE7LJyQbQtdV8U9Tc05PkAl2a'
CONSUMER_KEY = 'nsRkI1DCQkhD07WsJXSfJ0ue4'
CONSUMER_SECRET = 'temLXQ0yxbOdoqLAB7lsSUd3j6FSxkkPKkykwzWINLpGZhgHTa'

# Setup access to API
def connect_to_twitter_OAuth():
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	api = tweepy.API(auth)
	return api

def get_tweet(twitter_handle):
	tweets = api.user_timeline(screen_name=twitter_handle, 
			# 200 is the maximum allowed count
			count=1,
			include_rts = False,
			# Necessary to keep full_text 
			# otherwise only the first 140 words are extracted
			tweet_mode = 'extended'
			)
	for info in tweets:
		#print("ID: {}".format(info.id))
		#print(info.created_at)
		#print(info.full_text)
		#print("\n")

		now = datetime.now()
		difference = (now - info.created_at)
		total_days = abs((info.created_at - now).days)-1
		total_seconds = abs(difference.total_seconds() - 3*60*60)
		print("D: ", total_days, "S: ", total_seconds)
		return info.id, info.created_at, info.full_text, total_seconds


api = connect_to_twitter_OAuth() # Create API object

#public_tweets = api.home_timeline()

print("Tweepy version: " + tweepy.__version__)



# Firebase Config
cred = credentials.Certificate("firebase-sdk.json")
firebase_admin.initialize_app(cred, {
	'databaseURL': 'https://auth-development-265ec-default-rtdb.firebaseio.com'
})
ref = db.reference('/')
published_tweets = set()

try:
	while(1):
		db = ref.get()
		tasks = []

		for key, value in db.items():
			following = []
			for key2, value2 in value.items():
				following.append(value2)
			tasks.append(following)
		
		for task in tasks:

			for i in range(len(task)):
				
				if i == 0:
					print("Phone: ", task[0])
				else:
					print(task[i][1:])
					twit_id, date, full_text, time_passed = get_tweet(task[i][1:])

					key_str = str(task[0]) + str(twit_id)
					if not key_str in published_tweets and time_passed < 10:
						print("VALID ***************************************** SENDING SMS")
						published_tweets.add(key_str)
						send_SMS(task[i] , full_text, task[0])
	


		print("CYCLE COMPLETED ====================================")

except KeyboardInterrupt:
	print("Server terminated with Ctrl-C")
	pass	

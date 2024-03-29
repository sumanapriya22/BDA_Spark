import pykafka
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import twitter_config
from afinn import Afinn


#Keys for authentication

consumer_key = twitter_config.consumer_key
consumer_secret = twitter_config.consumer_secret
access_token = twitter_config.access_token
access_secret = twitter_config.access_secret

# Setting authentication to twitter

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# Class to send data to kafka
class KafkaPushListener(StreamListener):       
	#Initializing
	def __init__(self):
		self.client = pykafka.KafkaClient("localhost:9092")

		self.producer = self.client.topics[bytes("BDA_Spark", "ascii")].get_producer()
  
	#Simple transformation of data to filter only the tweet from the data we get from twitter and send it to kafka
	def on_data(self, data):
 		try:
 			json_data = json.loads(data)

 			send_data = '{}'
 			json_send_data = json.loads(send_data)			
 			json_send_data['text'] = json_data['text']

 			print(json_send_data['text'])

 			self.producer.produce(bytes(json.dumps(json_send_data),'ascii'))
 			return True
 		except KeyError:
 			return True
                                   
	#Method to print the status of error
	def on_error(self, status):
		print(status)
		return True

print("Starting")
twitter_stream = Stream(auth, KafkaPushListener())


twitter_stream.filter(track=['COVID-19'], languages=['en'])

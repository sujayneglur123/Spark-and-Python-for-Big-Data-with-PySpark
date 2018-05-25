import tweepy
from tweepy import OAuthHandler,Stream
from tweepy.streaming import StreamListener
import socket
import json


# Set up your credentials
consumer_key='4KFijw9dhxZYZwTPJZ31MDU2r'
consumer_secret='JJV9C11bmKQcsPMEHpGXYQkwGLHK2bWfGpf8jxJZGxX8exoICU'
access_token ='806229699475152897RkXdpRG8zJcpnMncBAeb8nu1zzrRXDZ'
access_secret='1rdUDHLQvq5fPlFSGw2MltQ3kg9D9QsMc85W6QI7V6Jdg'

# Create a class to listen to the tweets with a function that sends data through a socket
class TweetsListener(StreamListener):

  # Connect with client data
  def __init__(self, csocket):
      self.client_socket = csocket
  
  # Use the json library to load in the data, grab the text message and send it through the socket. If there's an exception or an error just print it out
  def on_data(self, data):
      try:
          msg = json.loads( data )
          print( msg['text'].encode('utf-8')) # Print the message and ecode as utf-8 so that if emojis show up, it prints a blank instead of throwing an error
          self.client_socket.send( msg['text'].encode('utf-8') )
          return True
      except BaseException as e:
          print("Error on_data: %s" % str(e))
      return True

  def on_error(self, status):
      print(status)
      return True

# Using access keys to make a connection and launching the twitter stream, filtering out the tweets on 'soccer'
def sendData(c_socket):
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)

  twitter_stream = Stream(auth, TweetsListener(c_socket))
  twitter_stream.filter(track=['guitar']) # soccer is the topic we are tracking

if __name__ == "__main__":
  s = socket.socket()         # Create a socket object
  host = "127.0.0.1"          # Get local machine name
  port = 9998                 # Reserve a port for your connection service
  s.bind((host, port))        # Bind to the port

  print("Listening on port: %s" % str(port))

  s.listen(5)                 # Now wait for client connection.
  c, addr = s.accept()        # Establish connection with client.

  print( "Received request from: " + str( addr ) )

  sendData( c )		      # Send the data to the client socket

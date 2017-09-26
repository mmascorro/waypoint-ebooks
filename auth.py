from requests_oauthlib import OAuth1Session
import yaml

with open('./config.yaml', 'r') as yaml_file:
    config = yaml.load(yaml_file)

consumer_key = config['twitter']['consumer_key']
consumer_secret = config['twitter']['consumer_secret']

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authenticate_url = 'https://api.twitter.com/oauth/authenticate'
authorize_url = 'https://api.twitter.com/oauth/authorize'

twitter = OAuth1Session(client_key = consumer_key, client_secret = consumer_secret)
twitter.fetch_request_token(request_token_url)
auth_url = twitter.authorization_url(authenticate_url)
print('Go to this url and then enter the PIN shown:')
print(auth_url)
pin = input('PIN from :')

access_token = twitter.fetch_access_token(access_token_url, verifier = pin)

config['twitter']['access_token'] = access_token['oauth_token']
config['twitter']['access_token_secret'] = access_token['oauth_token_secret']

yaml_file = open('./config.yaml', 'w')
yaml.dump(config, yaml_file, default_flow_style=False)

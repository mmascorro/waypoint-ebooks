import twitter
import yaml
import sqlite3
import time
import datetime

with open('./config.yaml', 'r') as yaml_file:
    config = yaml.load(yaml_file)

api = twitter.Api(consumer_key = config['twitter']['consumer_key'],
    consumer_secret = config['twitter']['consumer_secret'],
    access_token_key = config['twitter']['access_token'],
    access_token_secret = config['twitter']['access_token_secret']
)

conn = sqlite3.connect('./data/tweets.sqlite3')
c = conn.cursor()
c.execute('SELECT * FROM tweets WHERE posted = 0 ORDER BY id ASC')
post = c.fetchone()

status = api.PostUpdate(post[1])

dt = datetime.datetime.strptime(status.created_at,'%a %b %d %H:%M:%S %z %Y')
timestamp = dt.timestamp()

c.execute('UPDATE tweets SET posted = 1, posted_timestamp = ? WHERE id = ?', (timestamp, post[0]))

conn.commit()
conn.close()

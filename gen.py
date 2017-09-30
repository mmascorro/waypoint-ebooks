import markovify
import argparse
import sqlite3
import time

modelFile = './data/model.json'
corpusFile = './data/corpus.txt'
dbFile = './data/tweets.sqlite3'

def generate():
	generate_count = 96
	model_json = open(modelFile, 'r').read()
	model = markovify.Text.from_json(model_json)

	conn = sqlite3.connect(dbFile)
	c = conn.cursor()

	for i in range(generate_count):
		content = model.make_short_sentence(140)
		generated_timestamp = int(time.time())

		c.execute('INSERT INTO tweets (content,generated_timestamp) VALUES (?,?)', (content,generated_timestamp))
		print(content)
		print(generated_timestamp)
		print('----------')

		conn.commit()

	conn.close()




def make_model():
	corpus = open(corpusFile).read()

	text_model = markovify.Text(corpus, state_size=3)
	model_json = text_model.to_json()

	f = open(modelFile, mode='w')
	f.write(model_json)
	f.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--model", action="store_true", default=False, help="Create Model JSON")
	args = parser.parse_args()
	if args.model:
		make_model()
	else:
		generate()

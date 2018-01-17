import markovify
import argparse
import sqlite3
import time

modelFile = './data/model.json'
corpusFile = './data/corpus.txt'
dbFile = './data/tweets.sqlite3'

def generate():
    generate_count = 168
    model_json = open(modelFile, 'r').read()
    model = markovify.Text.from_json(model_json)

    conn = sqlite3.connect(dbFile)
    c = conn.cursor()

    for i in range(generate_count):
        content = model.make_short_sentence(140)
        generated_timestamp = int(time.time())

        if content:
            c.execute('INSERT INTO tweets (content,generated_timestamp) VALUES (?,?)', (content,generated_timestamp))
            print(content)
            print(generated_timestamp)
            print('----------')

            conn.commit()

    conn.close()

def make_model():
    corpus = open(corpusFile).read()

    text_model = markovify.Text(corpus, state_size=4)
    model_json = text_model.to_json()

    f = open(modelFile, mode='w')
    f.write(model_json)
    f.close()


def full_gen():
    corpus = open(corpusFile).read()

    model = markovify.Text(corpus, state_size=4)

    generate_count = 168

    conn = sqlite3.connect(dbFile)
    c = conn.cursor()

    for i in range(generate_count):
        content = model.make_short_sentence(140, max_overlap_ratio=.8)
        generated_timestamp = int(time.time())

        if content:
            c.execute('INSERT INTO tweets (content,generated_timestamp) VALUES (?,?)', (content,generated_timestamp))
            print(content)
            print(generated_timestamp)
            print('----------')

            conn.commit()

    conn.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", action="store_true", default=False, help="Create Model JSON")
    parser.add_argument("--gen", action="store_true", default=False, help="Generate from stored Model")
    parser.add_argument("--full", action="store_true", default=False, help="Full Geneate")
    args = parser.parse_args()
    if args.gen:
        generate()
    elif args.model:
        make_model()
    else:
        full_gen()

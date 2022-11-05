#!/usr/bin/python

import redis
import sys
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
nltk.download('stopwords')


redis_conn = redis.Redis(
        host='127.0.0.1',
        port=6379)

file_path = sys.argv[1]


with open (file_path, 'r') as f:
        text_file = f.read()

tokenizer = RegexpTokenizer(r'\w+')
text_tokens = tokenizer.tokenize(text_file)
text_tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]


for token in text_tokens_without_sw:
        redis_conn.zincrby("word_count_sample", 1, token)

sorted_set_ranked = redis_conn.zrevrangebyscore('word_count_sample', min='-inf', max='+inf', withscores=True)
for token in sorted_set_ranked:
        print(f'{token[0].decode("utf-8")} {int(token[1])}')

redis_conn.delete("word_count_sample")

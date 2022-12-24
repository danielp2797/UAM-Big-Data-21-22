#!/usr/bin/env python

import logging
import threading, multiprocessing
import requests
from bs4 import BeautifulSoup
import time
from kafka import KafkaConsumer, KafkaProducer
import json
import pdb
#pdb.set_trace()

## Logging
logging.basicConfig(
    filename='cooker.log',
    level=logging.INFO, 
    format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S'
)
# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

## Cooker
url = 'https://www.recetario.es'
raw_topic_name = 'recipes' # set topic name
raw_key = 'raw'
bootstrap_servers = 'localhost:9092' # set bootstrap server

def fetch_raw(recipe_url):
    html = None
    logging.info('Processing {}'.format(recipe_url))
    try:
        req = requests.get(recipe_url, verify=False)
        if req.status_code == 200:
            html = req.content
    except Exception as ex:
        logging.error('Exception while accessing raw html')
        logging.error(ex)
    finally:
        return html


def get_recipes():
	recipies = []
	try:
		req = requests.get(url + '/categorias/potajes-y-platos-de-cuchara', verify=False)
		if req.status_code == 200:
			soup = BeautifulSoup(req.content,'lxml', from_encoding='utf-8')
 			links = soup.find_all('a', class_='item-link item-title')
 			idx = 0
			for link in links:
 				time.sleep(2)
				recipe = fetch_raw(url + link['href'])
				recipies.append(recipe)
				idx += 1
				if idx > 2:
					break
		else:
			logging.warning('Review access to: ' + url)
	except Exception as ex:
		logging.error('Exception in get_recipes')
		logging.error(ex)
	finally:
		return recipies

def connect_kafka_producer():
	producer = None
	try:
		producer = KafkaProducer(bootstrap_servers=[bootstrap_servers]) # set producer
	except Exception as ex:
		logging.error('Exception while connecting producer')
		logging.error(ex)
	finally:
		return producer

def connect_kafka_consumer():
        consumer = None
        try:
                consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers,
                 auto_offset_reset='earliest',
                 consumer_timeout_ms=1000,
                 group_id='procooker-group') # set consumer
                 
        except Exception as ex:
                logging.error('Exception while connecting consumer')
                logging.error(ex)
        finally:
                return consumer


def publish_message(producer, topic, key, value):
	try:
		producer.send(topic, key=bytes(key), value=bytes(value)) # set send message
		producer.flush(timeout=1000)
 		logging.debug('Message published successfully')
	except Exception as ex:
		logging.error('Exception while publishing message')
		logging.error(ex)

def parse_list(section):
	items=[]
	for s in section:
		text = s.text.strip()
		if text != '':
			items.append(" ".join(text.split()))
	return items

def parse(markup):
	recipe = None
	try:
		soup = BeautifulSoup(markup, 'lxml', from_encoding='utf-8')
		title = soup.select("h1 div.step-container a[href='javascript:;']")[0].text
		steps = parse_list(soup.select("ol.steps-list li[style='list-style-type:none'] ol li"))
		ingredients = parse_list(soup.select("li[itemprop='recipeIngredient']"))
		recipe = {'title': title, 'steps': steps, 'ingredients': ingredients}
	except Exception as ex:
		logging.error('Exception while parsing')
		logging.error(ex)
	finally:
		return json.dumps(recipe)

class Reader(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.stop_event = threading.Event()
	def stop(self):
		self.stop_event.set()
	def run(self):
		i = 0
		recipes = get_recipes()
		producer = connect_kafka_producer()
		if recipes and producer:
			while not self.stop_event.is_set() and i < len(recipes):
				publish_message(producer, raw_topic_name, raw_key, recipes[i])
				i+=1
				time.sleep(1)
			producer.close()
		logging.info('End reader')

class Parser(multiprocessing.Process):
	def __init__(self):
		multiprocessing.Process.__init__(self)
		self.stop_event = multiprocessing.Event()
 	def stop(self):
		self.stop_event.set()
	def run(self):
		consumer = connect_kafka_consumer()
		consumer.subscribe([raw_topic_name]) # set message subscription
		if consumer:
			while not self.stop_event.is_set():
				for message in consumer: # set where to iterate messages
					logging.info(parse(message.value)) # set message value
					if self.stop_event.is_set():
						break
		consumer.close()
		logging.info('End parser')

if __name__ == '__main__':
	tasks = [
		Reader(),
		Parser()
	]
	for task in tasks:
		task.start()

	time.sleep(20)
	for task in tasks:
		task.stop()

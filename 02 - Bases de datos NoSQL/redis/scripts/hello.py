#!/usr/bin/python

import redis
import sys

redis_conn = redis.Redis(
        host='127.0.0.1',
        port=6379)

def say_hello_from_key(key:str, arg: str):
	'''
	Descripcion: Saluda al usuario con una clave a una BD Redis 
	que contenga un string de saludo y lo concatena con el nombre
	del segundo argumento.
	'''
	assert redis_conn.exists(key),'key[1] not in db'
	key_value = redis_conn.get(key).decode("utf-8")
	result = f'{key_value} {arg}'

	return result

print(say_hello_from_key(sys.argv[1], sys.argv[2]))
#!/usr/bin/python

import redis
import sys

redis_conn = redis.Redis(
        host='127.0.0.1',
        port=6379)

key, arg = sys.argv[1], sys.argv[2]
assert redis_conn.exists(key),'key[1] not in db'

with open ('hello.lua') as f:
        lua_file = f.read()

        say_hello = redis_conn.register_script(lua_file)

result = say_hello(keys=[key], args=[arg], client=redis_conn)
print(result.decode("utf-8"))

local first_key = redis.call('get',KEYS[1])
if not tonumber(first_key) then return "bad type on key[1]" end
local second_argv = ARGV[1]
if not tonumber(second_argv) then return "bad type on key[2]" end
return tonumber(first_key) * tonumber(second_argv)

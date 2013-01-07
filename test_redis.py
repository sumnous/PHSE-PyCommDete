import redis

r = redis.StrictRedis(host='192.168.215.76', port=6379, db=0)
r1 = redis.StrictRedis(host='192.168.215.76', port=6379, db=1)

print len(r.keys())
print r.dbsize()
print r1.dbsize()

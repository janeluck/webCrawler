import redis
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0) #注意这里我使用的是redis.StrictRedis
r.set('key', 'value')
r.set('name', 'kingname') #添加新信息
r.append('name', ' is a super man.') #在原有信息的尾部添加信息
r.delete('name') #删除key
name = r.get('name')
print(name)
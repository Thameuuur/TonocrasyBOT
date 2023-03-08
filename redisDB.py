import redis
import hashlib
import random


redis_db = redis.Redis(host='localhost', port=6380,
                 db=0, password=None, socket_timeout=None)
    
def add_user(name):
    user_id = hashlib.md5((name + str(random.random())).encode()).hexdigest()
    redis_db.hset('users', user_id, name)
    return user_id
    
def remove_user(username):
    redis_db.hdel('users', get_user_ID(username))
    
def get_users():
    return redis_db.hgetall('users')
    
def get_user_ID(username):
    for key, value in redis_db.hscan_iter('users'):
        if value.decode() == username:
            return key.decode()
    return None
    
def user_exists(username):
    user_id = get_user_ID(username)
    if user_id is not None:
        return True
    else:
        return False


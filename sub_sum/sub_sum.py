import redis

SUBSCRIPTION_NAME = 'pub_sub_test'

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)
    p = r.pubsub()
    p.psubscribe(SUBSCRIPTION_NAME)
    
    for new_message in p.listen():
        print(new_message)
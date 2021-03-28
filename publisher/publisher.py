from time import perf_counter

import os
import time
import random
import redis

PUBLISH_RATE = int(os.getenv("PUB_RATE_PER_SECOND", 20))
REDIS_HOST = os.getenv("REDIS_HOST", 'localhost')
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
SUBSCRIPTION_NAME = os.getenv("SUBCRIPTION_NAME", 'pub_sub_test')

# python does not define a max integer value, but we'll define it as max of int here
INT_MAX = 2137483647

def publish_random_int(publish_period, subscription_name):
    redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    next_time = publish_period

    while True:
        # We use perf_counter because sleep is system dependant and not accurate
        # enough for our high rates, and datetime is expensive to run in a loop
        current_tick = perf_counter()

        if current_tick < next_time:
            continue
        
        next_time = current_tick + publish_period
        current_value = random.randint(-INT_MAX, INT_MAX)
        redis_connection.publish(subscription_name, current_value)           


if __name__ == "__main__":
    if PUBLISH_RATE == 0:
        exit("PUB_RATE_PER_SECOND cannot be 0")

    publish_period =  1 / PUBLISH_RATE

    publish_random_int(
        publish_period=publish_period, 
        subscription_name=SUBSCRIPTION_NAME
    )
    
from datetime import datetime, timedelta

import os
import time
import random
import redis
import sys

# python does not define a max integer value, but we'll define it as max of uint here
UINT_MAX = 4294967295

def publish_random_int(publish_period, subscription_name):
    redis_connection = redis.Redis(host='localhost', port=6379, db=0)

    while True:
        next_time = datetime.now() + timedelta(seconds=publish_period)

        current_value = random.randint(0, UINT_MAX)
        # print("publish {}".format(current_value))
        redis_connection.publish(subscription_name, current_value)

        # To account for time it took to send the message, we can't just do a raw sleep
        # Otherwise we'll always be a bit slower than we wanted to be
        time.sleep((next_time - datetime.now()).total_seconds())

if __name__ == "__main__":
    subscription_name = os.getenv("SUBCRIPTION_NAME", 'pub_sub_test')
    publish_rate = os.getenv("PUB_RATE_PER_SECOND", 20)
    publish_period =  1 / publish_rate

    publish_random_int(
        publish_period=publish_period, 
        subscription_name=subscription_name
    )
    
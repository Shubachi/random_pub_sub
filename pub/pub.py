from datetime import datetime, timedelta
import time
import random
import redis
import sys

# python does not define a max integer value, but we'll define it as max of uint here
UINT_MAX = 4294967295
PUBLISH_RATE_PER_SECOND = 20
SUBSCRIPTION_NAME = 'pub_sub_test'

g_connection = redis.Redis(host='localhost', port=6379, db=0)

def publish_random_int():
    global g_connection
    current_value = random.randint(0, UINT_MAX)
    # print("publish {}".format(current_value))
    g_connection.publish(SUBSCRIPTION_NAME, current_value)

def schedule_publisher():
    publish_period = 1 / PUBLISH_RATE_PER_SECOND
    while True:
        next_time = datetime.now() + timedelta(seconds=publish_period)

        publish_random_int()

        # To account for time it took to send the message, we can't just do a raw sleep
        # Otherwise we'll always be a bit slower than we wanted to be
        time.sleep((next_time - datetime.now()).total_seconds())

if __name__ == "__main__":
    schedule_publisher()
    
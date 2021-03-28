from datetime import datetime, timedelta
from threading import Thread, Lock

import os
import redis
import statistics
import time

REDIS_HOST = os.getenv("REDIS_HOST", 'localhost')
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REPORT_PERIOD = os.getenv("REPORT_PERIOD", 5)
SUBSCRIPTION_NAME = os.getenv("SUBCRIPTION_NAME", 'pub_sub_test')

g_current_values = []
g_mutex = Lock()

def subscriber():
    global g_current_values
    global g_mutex

    redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    subscription = redis_connection.pubsub()
    subscription.subscribe(SUBSCRIPTION_NAME)

    for new_message in subscription.listen():
        # Ignore any messages that aren't explicitly messages
        if new_message.get("type") != "message":
            continue
        
        with g_mutex:   
            try:
                g_current_values.append(int(new_message.get("data")))
            except ValueError:
                print("{} cannot be converted to an int".format(new_message.get("data")))
   

def output_and_reset():
    global g_current_values
    global g_mutex

    while True:
        next_time = datetime.now() + timedelta(seconds=REPORT_PERIOD)

        with g_mutex:
            if g_current_values:
                median = statistics.median(g_current_values)
            else:
                median = 0
            print("Median: {}".format(int(median)))
            g_current_values = []

        # We can use sleep here because of the longer 5 second sleep, where the
        # inaccuracies of the sleep don't matter as much
        time.sleep((next_time - datetime.now()).total_seconds())


if __name__ == "__main__":
    mean_thread = Thread(target=output_and_reset)
    mean_thread.start()

    # Joining the subscriber thread means main process won't end until
    # thread is done (never)
    subscriber_thread = Thread(target=subscriber)
    subscriber_thread.start()
    subscriber_thread.join()



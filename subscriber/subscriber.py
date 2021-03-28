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
SUBSCRIBER_TYPE = os.getenv("SUBSCRIBER_TYPE")

class Subscriber(object):
    def __init__(self):
        self.mutex = Lock()
        self.redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.subscription = self.redis_connection.pubsub()
        self.subscription.subscribe(SUBSCRIPTION_NAME)

    def handle_message(self, data):
        raise NotImplementedError

    def listener(self):
        for new_message in self.subscription.listen():
            # Ignore any messages that aren't explicitly messages
            if new_message.get("type") != "message":
                continue
            
            with self.mutex:   
                try:
                    data = int(new_message.get("data"))
                    self.handle_message(data)
                except ValueError:
                    print("{} cannot be converted to an int".format(new_message.get("data")))

    def handle_output(self):
        raise NotImplementedError

    def output(self):
        while True:
            next_time = datetime.now() + timedelta(seconds=REPORT_PERIOD)

            with self.mutex:
                self.handle_output()

            # We can use sleep here because of the longer 5 second sleep, where the
            # inaccuracies of the sleep don't matter as much
            time.sleep((next_time - datetime.now()).total_seconds())


class MedianSubscriber(Subscriber):
    def __init__(self):
        Subscriber.__init__(self)
        self.current_values = []

    def handle_message(self, data):
        self.current_values.append(data)

    def handle_output(self):
        if self.current_values:
            print(self.current_values)
            median = statistics.median(self.current_values)
        else:
            median = 0
            
        print("Median: {}".format(int(median)))
        self.current_values = [] 


class SumSubscriber(Subscriber):
    def __init__(self):
        Subscriber.__init__(self)
        self.sum = 0    

    def handle_message(self, data):
        self.sum = self.sum + data

    def handle_output(self):
        print("Sum: {}".format(self.sum))
        self.sum = 0        


if __name__ == "__main__":
    if SUBSCRIBER_TYPE == "SUM":
        subscriber = SumSubscriber()
    elif SUBSCRIBER_TYPE == "MEDIAN":
        subscriber = MedianSubscriber()
    else:
        exit("Invalid SUBSCRIBER_TYPE {}".format(SUBSCRIBER_TYPE))

    output_thread = Thread(target=subscriber.output)
    output_thread.start()

    # Joining the subscriber thread means main process won't end until
    # thread is done (never)
    listener_thread = Thread(target=subscriber.listener)
    listener_thread.start()
    listener_thread.join()

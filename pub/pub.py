from apscheduler.schedulers.blocking import BlockingScheduler 

import redis

alice_r = redis.Redis(host='localhost', port=6379, db=0)

def some_job():
    print("Every 2 seconds")


def publisher():
    scheduler = BlockingScheduler()
    scheduler.add_job(some_job, 'interval', seconds=2)
    scheduler.start()

def redis_test():
    alice_r.publish('classical_music', 'Alice Music')

if __name__ == "__main__":
    #publisher()
    redis_test()
    
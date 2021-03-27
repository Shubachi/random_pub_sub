from threading import Thread, Lock
import time


g_CurrentSum = 0
g_CurrentCount = 0
mutex = Lock()


def add():
    global g_CurrentSum
    global g_CurrentCount
    global mutex

    while True:
        with mutex:
            g_CurrentSum = g_CurrentSum + 2
            g_CurrentCount = g_CurrentCount + 1
            print("g_CurrentSum {}".format(g_CurrentSum))
        
        time.sleep(1)


def mean_and_reset():
    global g_CurrentSum
    global g_CurrentCount
    global mutex

    while True:
        with mutex:
            mean = g_CurrentSum / g_CurrentCount
            g_CurrentSum = 0
            g_CurrentCount = 0
            print("mean {}".format(mean))
        
        time.sleep(5)


if __name__ == "__main__":
    add_thread = Thread(target=add)
    mean_thread = Thread(target=mean_and_reset)
    add_thread.start()
    mean_thread.start()

    while True:
        time.sleep(1)

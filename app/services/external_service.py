import random
import time


def credit_bureau_check(data):

    # simulate latency
    time.sleep(1)

    # simulate failure
    if random.random() < 0.3:
        raise Exception("Credit bureau service unavailable")

    return True
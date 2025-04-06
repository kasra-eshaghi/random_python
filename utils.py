import random

def calculate_delay_time(mean, RANDOM = True):
    if RANDOM:
        return random.expovariate(1/mean)
    else:
        return mean
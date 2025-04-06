'''
This scrip simulates a valet parking system.
I uses a Store object to simulat ethe valet workers

'''


import simpy
import random
import matplotlib.pyplot as plt

from customer import *
from valet import *
from utils import *


def generate_customers(env, valet, CUSTOMER_PARAMS, INTER_ARRIVAL_TIME = 10):

    id = 0
    while (True):
        inter_arrival_time = calculate_delay_time(INTER_ARRIVAL_TIME, RANDOM)
        yield env.timeout(inter_arrival_time)

        Customer(id, env, valet, **CUSTOMER_PARAMS)

        id += 1

env = simpy.Environment()
DIAG = True
RANDOM = False
VALET_PARAMS = {
    "N_WORKERS": 1,
    "PARKING_TIME": 10,
    "RETRIEVAL_TIME": 10,
    "DIAG": DIAG,
    "RANDOM": RANDOM,
}
valet = Valet(env, **VALET_PARAMS)

CUSTOMER_PARAMS = {
    "SHOPPING_TIME": 15,
    "DIAG": DIAG,
    "RANDOM": RANDOM,
}

INTER_ARRIVAL_TIME = 10
env.process(generate_customers(env, valet, CUSTOMER_PARAMS, INTER_ARRIVAL_TIME))

env.run(100)








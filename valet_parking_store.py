'''
This scrip simulates a valet parking system.
I uses a Resource object to simulat ethe valet workers

'''


import simpy
import random
import matplotlib.pyplot as plt

# Customer class
class Valet:
    def __init__(self, env, N_WORKERS = 5, PARKING_TIME = 10, RETRIEVAL_TIME = 10, DIAG = True, RANDOM = True):
        self.env = env
        self.workers = simpy.Resource(self.env, N_WORKERS)

        # process parameters
        self.PARKING_TIME = PARKING_TIME
        self.RETRIEVAL_TIME = RETRIEVAL_TIME

        # diagnostics
        self.DIAG = DIAG
        self.RANDOM = RANDOM

    def __repr__(self):
        return f'{self.__class__.__name__} {"Kasra"}'
        

    def parking_process(self, request):
        self.diag("Valet parking car")
        # park car
        parking_time = calculate_delay_time(self.PARKING_TIME, self.RANDOM)
        yield self.env.timeout(parking_time)

        # release valet
        self.workers.release(request)
        self.diag("Valet finished parking")

    def retrieval_process(self):
        self.diag("Valet retrieving car")
        retrieval_time = calculate_delay_time(self.RETRIEVAL_TIME, self.RANDOM)
        yield self.env.timeout(retrieval_time)
        self.diag("Valent finished retrieving")

    def diag(self, message): # Diagnostic routine
        if self.DIAG:
            print( "{} @ {}".format(message, self.env.now))
    
class Customer:

    def __init__(self, id, env, valet, SHOPPING_TIME = 100, DIAG = True, RANDOM = True):
        # simulation objects
        self.id = id
        self.env = env
        self.valet = valet

        # simulation parameters
        self.SHOPPING_TIME = SHOPPING_TIME
        
        # diagnostics
        self.DIAG = DIAG
        self.RANDOM = RANDOM
        self.state = "in_parking_line"

        # performance measures
        self.waiting_time = 0

        # go shopping
        self.env.process(self.go_shopping())

    def __repr__(self):
        cls = self.__class__.__name__
        print("{} {}".format(cls, self.id))
        return 
    

    def go_shopping(self):
        t1 = self.env.now

        ## PARKING
        # Request resource for parking car
        self.diag("arrived at parking and requested a valet")
        request = self.valet.workers.request()
        yield request

        # run parking process
        self.env.process(self.valet.parking_process(request))

        t2 = self.env.now

        # SHOPPING
        self.state = "shopping"
        self.diag("dropped off car, now going shopping")
        shopping_time = calculate_delay_time(self.SHOPPING_TIME, self.RANDOM)
        yield self.env.timeout(shopping_time)

        t3 = self.env.now

        ## BACK FROM SHOPPING
        self.state = "in_retrieval_line"
        self.diag("finished shopping and waiting for car")
        request = self.valet.workers.request()
        yield request

        # run retrieval process
        yield self.env.process(self.valet.retrieval_process())

        # release resource
        self.valet.workers.release(request)

        t4 = self.env.now

        # go home 
        self.state = "home"
        self.diag("going home")

        self.waiting_time += t4 - t3 + t2 - t1

        return

    def diag(self, message): # Diagnostic routine
        if self.DIAG:
            print( "Customer {} {} @ {}".format(self.id, message, self.env.now))

def calculate_delay_time(mean, RANDOM = True):
    if RANDOM:
        return random.expovariate(1/mean)
    else:
        return mean

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








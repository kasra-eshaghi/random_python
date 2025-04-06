import simpy

from utils import *

class Worker:
    def __init__(self, id):
        self.id = id
        self.state = "waiting_at_parking_entrance"
        """
        states: waiting_at_parking_entrance, waiting_at_parking_exit, parking_car, retrieving_car
        """

    def __repr__(self):
        return f'Worker {self.id}'

class Valet:
    def __init__(self, env, N_WORKERS = 5, PARKING_TIME = 10, RETRIEVAL_TIME = 10, DIAG = True, RANDOM = True):
        self.env = env
        self.workers = simpy.Store(self.env, N_WORKERS)
        for id in range(N_WORKERS):
            self.workers.put(Worker(id))

        # process parameters
        self.PARKING_TIME = PARKING_TIME
        self.RETRIEVAL_TIME = RETRIEVAL_TIME

        # diagnostics
        self.DIAG = DIAG
        self.RANDOM = RANDOM     

    def parking_process(self, worker):
        self.diag(worker, "parking car")
        # park car
        parking_time = calculate_delay_time(self.PARKING_TIME, self.RANDOM)
        yield self.env.timeout(parking_time)

        # release valet
        yield self.workers.put(worker)
        self.diag(worker, "finished parking")

    def retrieval_process(self, worker):
        self.diag(worker, "retrieving car")
        retrieval_time = calculate_delay_time(self.RETRIEVAL_TIME, self.RANDOM)
        yield self.env.timeout(retrieval_time)
        self.diag(worker, "finished retrieving")

        yield self.workers.put(worker)

    def diag(self, worker, message): # Diagnostic routine
        if self.DIAG:
            print( "{} {} @ {}".format(worker, message, self.env.now))
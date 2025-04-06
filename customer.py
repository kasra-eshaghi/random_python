from utils import *

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
        """
        states: waiting_at_parking_entrance, shopping, waiting_at_parking_exit, home
        """

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
        worker = yield self.valet.workers.get()

        # run parking process
        self.env.process(self.valet.parking_process(worker))

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
        worker = yield self.valet.workers.get()

        # run retrieval process
        yield self.env.process(self.valet.retrieval_process(worker))

        # release resource
        # yield self.valet.workers.put(worker)

        t4 = self.env.now

        # go home 
        self.state = "home"
        self.diag("going home")

        self.waiting_time += t4 - t3 + t2 - t1

        return

    def diag(self, message): # Diagnostic routine
        if self.DIAG:
            print( "Customer {} {} @ {}".format(self.id, message, self.env.now))
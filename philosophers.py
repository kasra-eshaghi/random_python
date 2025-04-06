import simpy
import random

# Set up the plotting system
import matplotlib . pyplot as plt
import matplotlib
matplotlib.style.use("ggplot")


# philospher: thinks, then gets huntry and tries to pick up two chopsticks, and then eats until satistied and then returns to thinking
# states: Thinking (the initial state), Hungry, Hungry-With-One-Chopstick, and Eating
class Philosopher():
    T0 = 10 # mean thinking time 
    T1 = 10 # mean eating time
    DT = 1 # time to pick the other chopstick
    PORTION = 20 # Single meal size

    MAX_WAIT = 75

    def __init__(self, env, chopsticks, my_id, bowl = None, DIAG = False):
        self.env = env
        self.chopsticks = chopsticks
        self.my_id = my_id

        self.bowl = bowl # container with all the food in it. Runs out at some point

        self.waiting = 0
        self.DIAG = DIAG

        # register the process with the environment
        env.process(self.run_the_party())

    def get_hungry (self, meal_size): # Request the resources
        # START_HIGHLIGHT
        start_waiting = self.env.now
        # END_HIGHLIGHT
        self.diag("requested chopstick")
        rq1 = self.chopsticks[0].request()
        yield rq1

        self.diag("obtained chopstick")
        yield self.env.timeout(self.DT)

        self.diag ("requested another chopstick ")
        rq2 = self.chopsticks [1].request()
        yield rq2
        self.diag ("obtained another chopstick ")

        if self . bowl is not None :
            request = self . bowl . get ( meal_size )

            yield request | self . env . timeout ( self . MAX_WAIT )
            if request . processed :
                self . diag ( " reserved food " )
            else : # Timeout
                self . diag ( " gave up " )

                self . waiting += self . env . now - start_waiting
                yield simpy . Event ( self . env ). fail ( ValueError ( rq1 , rq2 ))

        self.waiting += self.env.now-start_waiting
        return rq1 , rq2


    def run_the_party (self): # Do everything ...
        meal_size = self . PORTION

        while True :
            # Thinking - achieved by yielding a timeout (random) 
            thinking_delay = random.expovariate(1/self.T0)
            yield self.env.timeout(thinking_delay)
            # Getting hungry - achieved by yielding the process of get_hungry
            get_hungry_p = self.env.process(self.get_hungry(meal_size))

            try :
                rq1 , rq2 = yield get_hungry_p
                yield self . env . timeout ( random . expovariate (1 / self . T1 ))
                meal_size = self . PORTION
            except ValueError as values : # Timeout
                rq1 , rq2 = values . args
                meal_size += self . PORTION


            # rq1 , rq2 = yield get_hungry_p
            # # Eating - achieved by yielding a timeout (random)
            # eating_delay = random.expovariate(1/self.T1)
            # yield self.env.timeout(eating_delay)
            # Done eating , put down the chopsticks
            self.chopsticks[0].release(rq1)
            self.chopsticks[1].release(rq2)
            self.diag("released the chopsticks")

    def diag (self,message): # Diagnostic routine
        if self.DIAG :
            print( "P {} {} @ {}".format(self.my_id, message, self.env.now))

class Chef ():
    T2 = 150
    def __init__ ( self , env , bowl ):
        self . env = env
        self . bowl = bowl
        env . process ( self . replenish ())
    def replenish ( self ):
        while True :
            yield self . env . timeout ( self . T2 )
            if self . bowl . level < self . bowl . capacity :
                yield self . bowl . put ( self . bowl . capacity - self . bowl . level )

def simulate (n, t):
    """
    Simulate the system of n philosophers for up to t time units .
    Return the average waiting time .
    """
    env = simpy.Environment ()

    rice_bowl = simpy . Container ( env , init =1000 , capacity =1000)
    chef = Chef ( env , rice_bowl )


    chopsticks = [simpy.Resource(env, capacity= 1) for i in range (n)]
    philosophers = [Philosopher(env,(chopsticks[i], chopsticks[(i+1) % n]), i, rice_bowl) for i in range(n)]
    env.run(until=t)
    return sum(ph.waiting for ph in philosophers)/n

# n = 5
# t = 50
# wait_time = simulate(n, t)


N = 20
X = range (2, N)
Y = [simulate(n, 50000) for n in X]

plt.plot (X, Y, "-o")
plt.ylabel ("Waiting time")
plt.xlabel ("Number of philosophers")
plt.show()
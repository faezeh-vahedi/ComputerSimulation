
import matplotlib.pyplot as plt
import simpy
import numpy as np


def generate_interarrival():
    return np.random.exponential(1./3.0)


def generate_service():
    return np.random.exponential(1./4.0)


def cafe_run(env, servers):
    i = 0
    while True:
        i += 1
        yield env.timeout(generate_interarrival())
        env.process(customer(env, i, servers))


wait_t = []


def customer(env, customer, servers):
    with servers.request() as request:
        t_arrival = env.now
        print(env.now, 'customer {} arrives', format(customer))
        yield request
        print(env.now, 'customer {} is being served', format(customer))
        yield env.timeout(generate_service())
        print(env.now, 'customer {} departs', format(customer))
        t_depart = env.now
        wait_t.append(t_depart-t_arrival)


obs_times = []
q_length = []


def observe(env, servers):
    while True:
        obs_times.append(env.now)
        q_length.append(len(servers.queue))
        yield env.timeout(1.0)


np.random.seed(1)

env = simpy.Environment()
servers = simpy.Resource(env, capacity=1)

env.process(cafe_run(env, servers))
env.process(observe(env, servers))


env.run(until=100)

plt.figure()
plt.hist(wait_t)
plt.xlabel("Waiting time (min)")
plt.xlabel("Number of customers")

plt.figure()
plt.step(obs_times, q_length, where='post')
plt.xlabel("Time (min)")
plt.ylabel("Queue length")

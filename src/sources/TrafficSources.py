import numpy as np

class TrafficSource:
    def __init__(self, env, rate, packet_size_func, server_queue, traffic_type):
        self.env = env
        self.rate = rate
        self.packet_size_func = packet_size_func
        self.server_queue = server_queue
        self.traffic_type = traffic_type
        self.env.process(self.run())

    def run(self):
        while True:
            interarrival_time = np.random.exponential(1 / self.rate)
            yield self.env.timeout(interarrival_time)
            packet_size = self.packet_size_func()
            arrival_time = self.env.now
            self.server_queue.put((arrival_time, packet_size), self.traffic_type)

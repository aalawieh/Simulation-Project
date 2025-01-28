from sources.Globals import response_times

class ServerQueue:
    def __init__(self, env, rate):
        self.env = env
        self.rate = rate
        self.queue = []
        self.busy = False
        self.env.process(self.run())

    def put(self, packet, traffic_type):
        arrival_time, size = packet
        self.queue.append((arrival_time, size, traffic_type))

    def run(self):
        while True:
            if self.queue:
                self.busy = True
                packet = self.queue.pop(0)
                arrival_time, size, traffic_type = packet
                service_time = size / self.rate
                yield self.env.timeout(service_time)
                response_time = self.env.now - arrival_time
                response_times[traffic_type].append(response_time)
            else:
                self.busy = False
                yield self.env.timeout(0.001)


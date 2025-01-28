import simpy
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st


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


def simulate(burstiness_factor):
    global response_times
    response_times = {"data": [], "voice": [], "video": []}

    env = simpy.Environment()
    server_queue = ServerQueue(env, rate=100e6)

    # Data traffic
    TrafficSource(env, rate=30e6 / 8000, 
                  packet_size_func=lambda: np.random.choice([400, 4000, 12000]), 
                  server_queue=server_queue, traffic_type="data")

    # Voice traffic
    TrafficSource(env, rate=20e6 / 8000, 
                  packet_size_func=lambda: 800, 
                  server_queue=server_queue, traffic_type="voice")

    # Video traffic
    def video_traffic(env, server_queue, burstiness_factor):
        average_rate = 30e6 / 8000  # Average rate (30 Mbps)
        on_duration = 0.001  # 1 ms ON period
        peak_rate = burstiness_factor * average_rate
        while True:
            # ON period
            end_time = env.now + on_duration
            while env.now < end_time:
                packet_size = 8000
                arrival_time = env.now
                server_queue.put((arrival_time, packet_size), "video")
                yield env.timeout(1 / peak_rate)
            
            # OFF period
            off_duration = on_duration * (burstiness_factor - 1)
            yield env.timeout(off_duration)

    env.process(video_traffic(env, server_queue, burstiness_factor))
    env.run(until=20)


def calculate_confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    stderr = st.sem(data) 
    margin_of_error = st.t.ppf((1 + confidence) / 2, n - 1) * stderr
    return mean, mean - margin_of_error, mean + margin_of_error


# Main simulation logic
burstiness_values = [1, 2, 4, 8]
mean_response_times = {"data": [], "voice": [], "video": []}
ci_response_times = {"data": [], "voice": [], "video": []}

for b in burstiness_values:
    response_times = {"data": [], "voice": [], "video": []}
    simulate(b)
    for traffic_type in mean_response_times:
        mean, lower_ci, upper_ci = calculate_confidence_interval(response_times[traffic_type])
        mean_response_times[traffic_type].append(mean)
        ci_response_times[traffic_type].append((lower_ci, upper_ci))

# Plotting the results
plt.figure(figsize=(8, 6))
for traffic_type, color in zip(["data", "voice", "video"], ["blue", "orange", "green"]):
    means = mean_response_times[traffic_type]
    cis = ci_response_times[traffic_type]
    lower_bounds = [ci[0] for ci in cis]
    upper_bounds = [ci[1] for ci in cis]

    plt.plot(burstiness_values, means, label=traffic_type, color=color, marker='o')
    plt.fill_between(burstiness_values, lower_bounds, upper_bounds, color=color, alpha=0.2)

plt.xlabel("Burstiness Factor (\u03b2)")
plt.ylabel("Mean Response Time (s)")
plt.title("Effect of Burstiness on Mean Response Times")
plt.legend()
plt.grid(True)
plt.show()

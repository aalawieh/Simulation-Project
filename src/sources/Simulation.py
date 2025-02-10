import simpy
import numpy as np
from sources.TrafficSources import TrafficSource
from sources.ServerQueue import ServerQueue
from sources.Globals import response_times

def simulate(burstiness_factor):
    response_times["data"].clear()
    response_times["voice"].clear()
    response_times["video"].clear()

    env = simpy.Environment()
    server_queue = ServerQueue(env, rate=100e6)

    TrafficSource(env, rate = 30e6 / 8000, packet_size_func=lambda: np.random.choice([400, 4000, 12000]), server_queue=server_queue, traffic_type="data")
    TrafficSource(env, rate = 20e6 / 8000, packet_size_func=lambda: 800, server_queue=server_queue, traffic_type="voice")

    def video_traffic(env, server_queue, burstiness_factor):
        average_rate = 30e6 / 8000
        on_duration = 0.001
        peak_rate = burstiness_factor * average_rate
        while True:
            end_time = env.now + on_duration
            while env.now < end_time:
                packet_size = 8000
                arrival_time = env.now
                server_queue.put((arrival_time, packet_size), "video")
                yield env.timeout(1 / peak_rate)
            off_duration = on_duration * (burstiness_factor - 1)
            yield env.timeout(off_duration)

    env.process(video_traffic(env, server_queue, burstiness_factor))
    env.run(until=20)

def calculate_confidence_interval(data, block_size, confidence=0.95):
    n = len(data)
    if n < block_size:
        raise ValueError("Not enough data points for the chosen block size.")
    
    num_blocks = n // block_size
    blocks = [data[i * block_size:(i + 1) * block_size] for i in range(num_blocks)]
    block_means = [np.mean(block) for block in blocks]
    mean_of_means = np.mean(block_means)
    sigma_t = np.std(block_means, ddof=1)
    margin_of_error = 4.5 * sigma_t / np.sqrt(num_blocks)
    return mean_of_means, mean_of_means - margin_of_error, mean_of_means + margin_of_error
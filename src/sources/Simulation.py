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

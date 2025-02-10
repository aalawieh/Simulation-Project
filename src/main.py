import os
import numpy as np
from sources.Simulation import simulate, calculate_confidence_interval
from sources.Globals import response_times
from sources.PlotResults import plot_results

def save_results(mean_response_times, ci_response_times, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)
    response_file = os.path.join(output_dir, "response_times.txt")
    
    with open(response_file, "w") as f:
        f.write("Traffic Type, Burstiness, Mean Response Time, Lower CI, Upper CI\n")
        for traffic_type in mean_response_times:
            for i, burstiness in enumerate(burstiness_values):
                mean = mean_response_times[traffic_type][i]
                lower_ci, upper_ci = ci_response_times[traffic_type][i]
                f.write(f"{traffic_type}, {burstiness}, {mean:.6f}, {lower_ci:.6f}, {upper_ci:.6f}\n")

burstiness_values = [ 1, 10 ,20, 30, 40, 50, 60, 70, 80, 90, 100]
mean_response_times = {"data": [], "voice": [], "video": []}
ci_response_times = {"data": [], "voice": [], "video": []}

for b in burstiness_values:
    simulate(b)
    for traffic_type in mean_response_times:
        mean, lower_ci, upper_ci = calculate_confidence_interval(response_times[traffic_type], block_size=50)
        mean_response_times[traffic_type].append(mean)
        ci_response_times[traffic_type].append((lower_ci, upper_ci))

save_results(mean_response_times, ci_response_times)
plot_results(burstiness_values, mean_response_times, ci_response_times)

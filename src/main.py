import os
import numpy as np
import scipy.stats as st
from sources.Simulation import simulate
from sources.Globals import response_times
from sources.PlotResults import plot_results


def calculate_confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    stderr = st.sem(data)
    margin_of_error = st.t.ppf((1 + confidence) / 2, n - 1) * stderr
    return mean, mean - margin_of_error, mean + margin_of_error


# Save results to files
def save_results(mean_response_times, ci_response_times, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)

    # Save response time data
    response_file = os.path.join(output_dir, "response_times.txt")
    with open(response_file, "w") as f:
        f.write("Traffic Type, Burstiness, Mean Response Time, Lower CI, Upper CI\n")
        for traffic_type in mean_response_times:
            for i, burstiness in enumerate(burstiness_values):
                mean = mean_response_times[traffic_type][i]
                lower_ci, upper_ci = ci_response_times[traffic_type][i]
                f.write(f"{traffic_type}, {burstiness}, {mean:.6f}, {lower_ci:.6f}, {upper_ci:.6f}\n")
    print(f"Response times saved to: {response_file}")


# Main simulation logic
burstiness_values = [1, 2, 4, 8]
mean_response_times = {"data": [], "voice": [], "video": []}
ci_response_times = {"data": [], "voice": [], "video": []}

for b in burstiness_values:
    simulate(b)
    for traffic_type in mean_response_times:
        mean, lower_ci, upper_ci = calculate_confidence_interval(response_times[traffic_type])
        mean_response_times[traffic_type].append(mean)
        ci_response_times[traffic_type].append((lower_ci, upper_ci))

# Save results and plot
save_results(mean_response_times, ci_response_times)
plot_results(burstiness_values, mean_response_times, ci_response_times)

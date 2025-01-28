import matplotlib.pyplot as plt
import os

def plot_results(burstiness_values, mean_response_times, ci_response_times, output_dir="results"):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Plot the results
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

    # Save the plot
    plot_path = os.path.join(output_dir, "burstiness_vs_response_times.png")
    plt.savefig(plot_path)
    print(f"Plot saved to: {plot_path}")

    plt.show()

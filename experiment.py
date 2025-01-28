import time
import matplotlib.pyplot as plt
from Functies.baseline import baseline
from Functies.read_files import read_data
import csv

# Paths for station and connection data
stations_file = 'Data/StationsNationaal.csv'
connections_file = 'Data/ConnectiesNationaal.csv'

# Algorithms to compare
algorithms = ['Random', 'Greedy', 'DepthFirst', 'SimulatedAnnealing', 'HillClimber']

# Parameters for the experiment, max_time in sec
min_trajects = 1
max_trajects = 20
iterations = 1500000
max_time = 10
visualize_condition = False
time_limit = 180

# Read station and connection data
stations_data, connections_data = read_data(stations_file, connections_file)

# Store results
results = {}
iteration_counts = {}

# Run experiments for each algorithm
for algorithm in algorithms:
    print(f"\nRunning experiment for algorithm: {algorithm}")

    # Initialize tracking
    highest_quality = 0
    time_intervals = []
    quality_over_time = []

    start_time = time.time()
    elapsed_time = 0

    iteration = 0
    with open(f"Experiment_{algorithm}.csv", 'w') as f:

        writer = csv.writer(f)
        writer.writerow(['elapsed_time', 'highest_quality', 'iteration'])

        while elapsed_time < max_time:
            # Run one iteration of the algorithm
            if algorithm == 'SimulatedAnnealing':
                quality_dict, highest_score, best_trajects = baseline(
                    iterations=1,
                    traject_type=algorithm,
                    min_trajects=min_trajects,
                    max_trajects=max_trajects,
                    stations_file=stations_file,
                    connections_file=connections_file,
                    DFS_depth=None,
                    algorithm_iterations=10000,
                    time_limit=time_limit)

            elif algorithm == 'HillClimber':
                quality_dict, highest_score, best_trajects = baseline(
                    iterations=1,
                    traject_type=algorithm,
                    min_trajects=min_trajects,
                    max_trajects=max_trajects,
                    stations_file=stations_file,
                    connections_file=connections_file,
                    DFS_depth=None,
                    algorithm_iterations=10000,
                    time_limit=time_limit)
            elif algorithm == 'DepthFirst':
                quality_dict, highest_score, best_trajects = baseline(
                    iterations=1,
                    traject_type=algorithm,
                    min_trajects=min_trajects,
                    max_trajects=max_trajects,
                    stations_file=stations_file,
                    connections_file=connections_file,
                    DFS_depth=22,
                    algorithm_iterations=None,
                    time_limit=time_limit)
            else:
                quality_dict, highest_score, best_trajects = baseline(
                    iterations=1,
                    traject_type=algorithm,
                    min_trajects=min_trajects,
                    max_trajects=max_trajects,
                    stations_file=stations_file,
                    connections_file=connections_file,
                    DFS_depth=None,
                    algorithm_iterations=None,
                    time_limit=time_limit)

            # Update the highest quality if the current score is better
            if highest_score > highest_quality:
                highest_quality = highest_score

            # Track elapsed time
            elapsed_time = int(time.time() - start_time)

            # Record data at every second
            if len(time_intervals) == 0 or elapsed_time > time_intervals[-1]:
                time_intervals.append(elapsed_time)
                quality_over_time.append(highest_quality)

            # Increment iteration count
            iteration += 1
            if iteration >= iterations:
                break

            writer.writerow([elapsed_time, highest_quality, iteration])

    # Store results for the algorithm
    results[algorithm] = {'time_intervals': time_intervals, 'quality_over_time': quality_over_time}

    # Store the total iterations
    iteration_counts[algorithm] = iteration

    # Print progress
    print(f"Completed {algorithm}: {len(time_intervals)} seconds tracked, {iteration} iterations completed.")

# Plot quality vs. time for each algorithm
plt.figure(figsize=(12, 8))

for algorithm, data in results.items():
    total_iterations = iteration_counts[algorithm]
    plt.plot(
        data['time_intervals'],
        data['quality_over_time'],
        label=f"{algorithm} ({total_iterations} iterations)",
        marker='o',
        linestyle='-',
        markersize=3)

plt.xlabel('Time (seconds)')
plt.ylabel('Highest Quality (Score)')
plt.title('Quality vs. Time for All Algorithms')
plt.legend(loc='lower right', fontsize=10)
plt.grid(True)
plt.show()

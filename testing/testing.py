from Functies.random_multiple_trajects import random_multiple_trajects
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# For the baseline file

def baseline(iterations):
    cost_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
    for i in range(iterations):
        nr, trajects, cost = random_multiple_trajects(1, 7)
        cost_dict[nr].append(cost)


def collect_baselines(iterations, num_runs):
    """
    Collect the results from multiple baseline runs, interchangable.
    And it returns list of dictionaries with results from each baseline run.
    """
    # List of dicts for baseline costs.
    all_results = []
    for run in range(num_runs):

        # Cost dictionary per baseline
        cost_dict = baseline(iterations)
        all_results.append(cost_dict)

    return all_results


def plot_multiple_baselines(all_results, labels, iterations):
    """
    Plots multiple baseline results on the same graph.
    all_results is a list of dictionaries containing costs for each run.
    List of labels corresponding to each run.
    """
    plt.figure(figsize=(10, 6))

    for i, cost_dict in enumerate(all_results):
        avg_costs = [sum(cost_dict[k]) / len(cost_dict[k]) for k in range(1, 8)]

        plt.plot(range(1, 8), avg_costs, label=labels[i])

    plt.xlabel("Trajectories")
    plt.ylabel("Average Cost")
    plt.title(f"Baseline comparison for {iterations} Iterations")
    plt.legend()
    plt.grid(True)
    plt.show()



# For the main

# Parameters for baseline comparison
num_runs = 3
iterations = 100

# Collect baseline results
all_results = collect_baselines(iterations, num_runs)
labels = [f"Run {i+1}" for i in range(num_runs)]
plot_multiple_baselines(all_results, labels, iterations)

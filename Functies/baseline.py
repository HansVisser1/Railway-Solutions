from Functies.random_multiple_trajects import random_multiple_trajects
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

def baseline(iterations):
    quality_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
    for i in range(iterations):
        nr, trajects, quality = random_multiple_trajects(1, 7)
        quality_dict[nr].append(quality)

    return quality_dict


def collect_baselines(iterations, num_runs):
    """
    Collect the results from multiple baseline runs, interchangable how many.
    And it returns list of dictionaries with results from each baseline run.
    """
    # List of dicts for baseline costs.
    all_results = []
    for run in range(num_runs):

        # Cost dictionary per baseline
        quality_dict = baseline(iterations)
        all_results.append(quality_dict)

    return all_results


def plot_multiple_baselines(all_results, labels, iterations):
    """
    Plots multiple baseline results on the same graph.
    all_results is a list of dictionaries containing costs for each run.
    List of labels corresponding to each run.
    On the x-axis the trajectories 1 to 7 and on the y axis the average cost.
    """
    plt.figure(figsize=(10, 6))

    for i, quality_dict in enumerate(all_results):
        avg_quality = [sum(quality_dict[k]) / len(quality_dict[k]) for k in range(1, 8)]

        plt.plot(range(1, 8), avg_quality, label=labels[i])

    plt.xlabel("Trajectories")
    plt.ylabel("Average Quality")
    plt.title(f"Baseline comparison for {iterations} Iterations")
    plt.legend()
    plt.grid(True)
    plt.show()

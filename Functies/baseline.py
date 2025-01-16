from Functies.random_multiple_trajects import random_multiple_trajects
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt


def baseline(iterations, traject_type, min_trajects, max_trajects, stations_file, connections_file, DFS_depth):
    """
    Run a baseline trajectory generation multiple times and collect quality scores.
    """
    quality_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
    for i in range(iterations):
        nr, trajects, quality = random_multiple_trajects(traject_type, min_trajects, max_trajects, stations_file, connections_file, DFS_depth)
        quality_dict[nr].append(quality)

    return quality_dict


def collect_baselines(iterations, traject_type, num_runs, min_trajects, max_trajects, stations_file, connections_file, DFS_depth):
    """
    Collect the results from multiple baseline runs, interchangable how many.
    And it returns list of dictionaries with results from each baseline run.
    """
    all_results = []
    for run in range(num_runs):
        quality_dict = baseline(
            iterations, traject_type, min_trajects, max_trajects, stations_file, connections_file, DFS_depth)
        all_results.append(quality_dict)

    return all_results


def plot_quality_distribution(all_results, iterations):
    """
    Plot the distribution of quality scores for each trajectory count (1-7).
    Creates separate histograms or KDEs for each trajectory count.
    """
    plt.figure(figsize=(12, 8))

    # Flatten the data into a list of (trajectory count, quality) pairs
    qualities = []
    for quality_dict in all_results:
        for k, values in quality_dict.items():
            for value in values:
                qualities.append((k, value))

    # Create a DataFrame for easier plotting
    df = pd.DataFrame(qualities, columns=["Trajectories", "Quality"])
    print(len(qualities))
    # Plot histograms for each trajectory count
    sns.histplot(data=df, x="Quality", hue="Trajectories", multiple="stack", bins=100, legend=True)

    plt.xlabel("Quality")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of Quality Scores Across {iterations} Iterations")
    # plt.legend(title="Trajectories")
    plt.grid(True)
    plt.show()

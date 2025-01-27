from Functies.random_multiple_trajects import random_multiple_trajects
from Functies.highest_score_convert import highest_score_convert
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import time



def baseline(iterations, traject_type, min_trajects, max_trajects, stations_file, connections_file, DFS_depth, algorithm_iterations, time_limit):
    """
    Run a baseline trajectory generation multiple times and collect quality scores.
    """
    quality_dict = {}
    highest_score = int(-10000)
    best_trajects = None
    for i in range(min_trajects, max_trajects + 1):
        quality_dict[i] = []

    start = time.perf_counter()
    for i in range(iterations):
        nr, trajects, quality = random_multiple_trajects(traject_type, min_trajects, max_trajects, stations_file, connections_file, DFS_depth, algorithm_iterations, time_limit)

        quality_dict[nr].append(quality)
        if i % 100 == 0:
            pass
        print(f"iteration {i}/{iterations}")

        # Update the highest score if this run's score is better
        if quality > highest_score:
            highest_score = quality
            best_trajects = trajects

        end = time.perf_counter()
        if traject_type == 'DepthFirst' or traject_type == 'SimulatedAnnealing':
            if (end - start) < 60:
                print(f"The experiment has been running for {int(end - start)} seconds")
            elif 120 > (end - start) > 60:
                print(f"The experiment has been running for {int((end - start) / 60)} minute and {int((end - start) % 60)} seconds")
            else:
                print(f"The experiment has been running for {int((end - start) / 60)} minutes and {int((end - start) % 60)} seconds")


    # Print the best result
    print(f"\nThe highest quality score achieved with the {traject_type} algorithm is: {highest_score}")
    print("Best trajectory solution:")


    if traject_type == 'DepthFirst':
        for i, (key, traject) in enumerate(best_trajects.items(), start=1):
            print(f"Traject {i}:")
            for step in traject:
                print(step)
            print()

    elif traject_type == 'HillClimber' or traject_type == 'SimulatedAnnealing':
        count = 1
        for traject in best_trajects:
            print(f"Traject {count}:")
            print(traject)
            print()
            count += 1
    else:
        for i, traject in enumerate(best_trajects, start=1):
            print(f"Traject {i}:")
            for step in traject.connections:
                print(step)
            print()

    return quality_dict, highest_score, best_trajects



def collect_baselines(iterations, traject_type, num_runs, min_trajects, max_trajects, stations_file, connections_file, DFS_depth, algorithm_iterations, time_limit):
    """
    Collect the results from multiple baseline runs, interchangable how many.
    And it returns list of dictionaries with results from each baseline run.
    """
    all_results = []
    highest_score = int(-10000)

    for run in range(num_runs):
        quality_dict, run_highest_score, best_trajects = baseline(
            iterations, traject_type, min_trajects, max_trajects, stations_file, connections_file, DFS_depth, algorithm_iterations, time_limit)
        all_results.append(quality_dict)
        if run_highest_score > highest_score:
            highest_score = run_highest_score

    best_result = highest_score_convert(best_trajects, traject_type)


    return all_results, highest_score, best_result


def plot_quality_distribution(all_results, iterations, traject_type, highest_score):
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

    # Plot histograms for each trajectory count
    sns.histplot(data=df, x="Quality", hue="Trajectories", multiple="stack", bins=100, legend=True)

    # # Highlight highest score
    # plt.axvline(x=highest_score, color='red', linestyle='--', label=f'Highest Score: {highest_score}')
    # plt.legend()


    plt.xlabel("Quality")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of Quality Scores Across {iterations} Iterations, with the {traject_type} algorithm.")
    plt.grid(True)
    plt.show()

    sns.histplot(data=df, x="Quality", hue="Trajectories", multiple="stack", bins=100, legend=True, palette='coolwarm')

    # # Highlight highest score
    # plt.axvline(x=highest_score, color='red', linestyle='--', label=f'Highest Score: {highest_score}')
    # plt.legend()


    plt.xlabel("Quality")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of Quality Scores Across {iterations} Iterations, with the {traject_type} algorithm.")
    plt.grid(True)
    plt.show()

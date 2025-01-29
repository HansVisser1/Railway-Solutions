import pprint
from Functies.read_files import read_data
from Functies.baseline import baseline, collect_baselines, plot_quality_distribution
from Visualisation.visualize_railway import visualize_all_trajects

# the path should end in 'Nationaal.csv' for the whole of the Netherlands or 'Holland.csv' for north and south Holland.
stations = 'Data/StationsNationaal.csv'
connections = 'Data/ConnectiesNationaal.csv'

# select the minimum and maximum amount of trajects allowed for the network
min_trajects = 1
max_trajects = 20
time_limit = 180
visualize_condition = True

# possible types: 'DepthFirst', 'Random', 'Greedy', 'HillClimber', 'SimulatedAnnealing'
traject_type = 'Random'

# required for HillClimber and SimulatedAnnealing (iterations per )
algorithm_iterations = 2000

# required for depthfirst (the maximum possible amount of connections in a traject)
depthfirst_depth = 22

# check if input is correct
while traject_type not in ['DepthFirst', 'SimulatedAnnealing', 'Greedy', 'Random', 'HillClimber']:
    print(f"ERROR: Spelling of traject_type is incorrect, it should be one of these: {['DepthFirst', 'SimulatedAnnealing', 'Greedy', 'Random', 'HillClimber']}")
    break


# read the data for the visualization
station_dict, connection_dict = read_data(stations, connections)

# iterations for the baseline
iterations = 15000

# Collect baseline results
all_results, highest_score, best_trajects = collect_baselines(iterations, traject_type, num_runs=1, min_trajects, max_trajects, stations, connections, depthfirst_depth, algorithm_iterations, time_limit)

# plot_multiple_baselines(all_results, labels, iterations)
plot_quality_distribution(all_results, iterations, traject_type, highest_score)

# visualize the trajects
if visualize_condition == True:
    visualize_all_trajects(station_dict, best_trajects)

import pprint
from Functies.read_files import read_data
from Functies.random_multiple_trajects import random_multiple_trajects
from Functies.baseline import baseline, collect_baselines, plot_quality_distribution
from Functies.list_connections import list_connections
from Functies.DepthFirstTraject import DepthFirstTraject
from Visualisation.visualize_railway import visualize_all_trajects
from Functies.Traject import Traject
from Functies.greedy import GreedyTraject
from Functies.convert_station_list_to_connections import convert_station_list_to_connections
from Functies.traject_list  import traject_list
from Functies.highest_score_convert import highest_score_convert

stations = 'Data/StationsNationaal.csv'
connections = 'Data/ConnectiesNationaal.csv'
min_trajects = 1
max_trajects = 22
time_limit = 180
visualize_condition = True

# possible types: 'DepthFirst', 'Random', 'Greedy', 'HillClimber', 'SimulatedAnnealing'
traject_type = 'DepthFirst'

# required for HillClimber and SimulatedAnnealing
algorithm_iterations = 2000

# required for depthfirst
depthfirst_depth = 22

# check if input is correct
while traject_type not in ['DepthFirst', 'SimulatedAnnealing', 'Greedy', 'Random', 'HillClimber']:
    print(f"ERROR: Spelling of traject_type is incorrect, it should be one of these: {['DepthFirst', 'SimulatedAnnealing', 'Greedy', 'Random', 'HillClimber']}")
    break


# read the data for the visualization
station_dict, connection_dict = read_data(stations, connections)


#Parameters for baseline comparison
num_runs = 1

iterations = 500


# Collect baseline results
all_results, highest_score, best_trajects = collect_baselines(iterations, traject_type, num_runs, min_trajects, max_trajects, stations, connections, depthfirst_depth, algorithm_iterations, time_limit)
# labels = [f"Run {i+1}" for i in range(num_runs)]

# plot_multiple_baselines(all_results, labels, iterations)
plot_quality_distribution(all_results, iterations, traject_type, highest_score)


# visualize the trajects
if visualize_condition == True:
    visualize_all_trajects(station_dict, best_trajects)

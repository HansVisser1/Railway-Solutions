import pprint
import csv
from Functies.output_to_csv import output_to_csv
from Functies.read_files import read_data
from Functies.baseline import baseline, collect_baselines, plot_quality_distribution
from Visualisation.visualize_railway import visualize_all_trajects

# Nationaal / Holland
network = 'Nationaal'

# select the minimum and maximum amount of trajects allowed for the network
min_trajects = 1
max_trajects = 20
time_limit = 180
visualize_condition = True

# possible types: 'DepthFirst', 'Random', 'Greedy', 'HillClimber', 'SimulatedAnnealing'
traject_type = 'Random'

# iterations for the baseline
iterations = 300

# required for HillClimber and SimulatedAnnealing (iterations per model run)
algorithm_iterations = 2000

# required for depthfirst (the maximum possible amount of connections in a traject)
depthfirst_depth = 22

# check if input is correct
while traject_type not in ['DepthFirst', 'SimulatedAnnealing', 'Greedy', 'Random', 'HillClimber']:
    print(f"ERROR: Spelling of traject_type is incorrect, it should be one of these: {['DepthFirst', 'SimulatedAnnealing', 'Greedy', 'Random', 'HillClimber']}")
    break

# path to the files (DO NOT EDIT)
stations = f'Data/Stations{network}.csv'
connections = f'Data/Connecties{network}.csv'

# read the data for the visualization
station_dict, connection_dict = read_data(stations, connections)

# Collect baseline results
all_results, highest_score, best_trajects = collect_baselines(iterations, traject_type, 1, min_trajects, max_trajects, stations, connections, depthfirst_depth, algorithm_iterations, time_limit)

output_to_csv(best_trajects, highest_score, traject_type, network, iterations)

# plot_multiple_baselines(all_results, labels, iterations)
plot_quality_distribution(all_results, iterations, traject_type, highest_score)

# visualize the trajects
# arguments: (dict_stations, traject_list, file_name = None, province = True, save_figure = False, algorithm = 'Test', save_gif = False)
if visualize_condition == True:
    if network == 'Nationaal':
        province = True
    else:
        province = False
    visualize_all_trajects(station_dict, best_trajects, province)

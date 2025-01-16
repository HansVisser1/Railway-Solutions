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

# possible types: 'DepthFirst', 'Random', Greedy
traject_type = 'DepthFirst'

# create random number of trajects and return the nr of trajects, trajects objects list and the total cost
nr, trajects, quality = random_multiple_trajects(traject_type, 1, 7, 'Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv', 15)
pprint.pprint(trajects)
# make the connections_list for the visualization
if traject_type == 'DepthFirst':
    traject_list = []

    for key in trajects.keys():
        station_list= []
        station_list = trajects[key]['stations']
        connection_list = convert_station_list_to_connections(station_list)

        for i in range(len(connection_list)):
            connection_list[i].append(0)
        traject_list.append(connection_list)
    # pprint.pprint(traject_list)

else:
    traject_list = list_connections(trajects)

count = 0
for traject in traject_list:
    count += 1
    pprint.pprint(f"Traject {count}: {traject}")
    print()
# read the data for the visualization
station_dict, connection_dict = read_data('Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv')

# visualize the trajects
visualize_all_trajects(station_dict, traject_list)

# Parameters for baseline comparison
num_runs = 4
iterations = 100

# Collect baseline results
all_results = collect_baselines(iterations, traject_type, num_runs, 1, 7, 'Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv', 15)
labels = [f"Run {i+1}" for i in range(num_runs)]
# plot_multiple_baselines(all_results, labels, iterations)
plot_quality_distribution(all_results, iterations)

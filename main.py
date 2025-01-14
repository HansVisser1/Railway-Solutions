import pprint
from Functies.read_files import read_data
from Functies.random_multiple_trajects import random_multiple_trajects
from Functies.baseline import baseline, collect_baselines, plot_multiple_baselines
from Functies.list_connections import list_connections
from Visualisation.visualize_railway import visualize_all_trajects

traject_type = 'Random'

# create random number of trajects and return the nr of trajects, trajects objects list and the total cost
nr, trajects, quality = random_multiple_trajects(traject_type, 1, 7, 'Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv')

# make the connections_list for the visualization
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
iterations = 150

# Collect baseline results
all_results = collect_baselines(iterations, traject_type, num_runs, 1, 7, 'Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv')
labels = [f"Run {i+1}" for i in range(num_runs)]
plot_multiple_baselines(all_results, labels, iterations)

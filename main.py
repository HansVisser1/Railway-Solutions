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

# possible types: 'DepthFirst', 'Random', Greedy
traject_type = 'DepthFirst'
visualize_condition = False


# create random number of trajects and return the nr of trajects, trajects objects list and the total cost
nr, trajects, quality = random_multiple_trajects(traject_type, 5, 5, 'Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv', 15)

traject_list = traject_list(trajects, traject_type)

# read the data for the visualization
station_dict, connection_dict = read_data('Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv')
#print(traject_list)

# visualize the trajects
if visualize_condition == True:
    visualize_all_trajects(station_dict, traject_list)

#Parameters for baseline comparison
num_runs = 1

iterations = 100


# Collect baseline results
all_results = collect_baselines(iterations, traject_type, num_runs, 1, 7, 'Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv', 15)
labels = [f"Run {i+1}" for i in range(num_runs)]
# plot_multiple_baselines(all_results, labels, iterations)
plot_quality_distribution(all_results, iterations, traject_type)

quality_dict = baseline(iterations, traject_type, 1, 7, 'Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv', 15)

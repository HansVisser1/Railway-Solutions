import pprint
from Functies.classes import Traject
from Functies.read_files import read_data
from Functies.random_multiple_trajects import random_multiple_trajects
from Functies.baseline import baseline
from Functies.list_connections import list_connections
from Visualisation.visualize_railway import visualize_traject

# create random number of trajects and return the nr of trajects, trajects objects list and the total cost
nr, trajects, cost = random_multiple_trajects(1, 7)

# make the connections_list for the visualization
connections_list = list_connections(trajects)

# read the data for the visualization
station_dict, connection_dict = read_data('Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv')

# visualize the trajects
visualize_traject(station_dict, trajects)

# baseline cost calculation
print(baseline(100))

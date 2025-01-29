from Functies.DepthFirstTraject import DepthFirstTraject
from Functies.convert_station_list_to_connections import convert_station_list_to_connections
from Functies.read_files import read_data
from Visualisation.visualize_railway import visualize_all_trajects
import pprint

depth_first = DepthFirstTraject()
depth_first.run('Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv')
depth_first.depth_first_search(15, 7)
trajects = depth_first.trajects
pprint.pprint(trajects)
trajects_list = []

for key in trajects.keys():
    station_list= []
    station_list = trajects[key]['stations']
    connection_list = convert_station_list_to_connections(station_list)

    for i in range(len(connection_list)):
        connection_list[i].append(0)
    trajects_list.append(connection_list)



# read the data for the visualization
station_dict, connection_dict = read_data('Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv')

# visualize the trajects
visualize_all_trajects(station_dict, trajects_list)

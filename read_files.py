import csv
import pprint
def read_data(stations_file, connections_file):
    """
    This function takes the stations file and the connections file
    Stations is a dictionary that has the station name as key, and the values are
    x, y and connections. Connections in turn is a dictionary of all the connections
    a certain station has.
    Connections here is a nested dictionary containing the info for its
    connections.
    """
    stations = {}
    connections = []


    # Reading stations using open
    with open(stations_file, 'r') as file:
        document = csv.DictReader(file)
        for row in document:
            station_name = row['station']
            x = row['x']
            y = row['y']
            stations[station_name] = {'x': x, 'y': y, 'connections': {}}

    # Reading connections using open
    with open(connections_file, 'r') as file:
        document = csv.DictReader(file)
        for row in document:
            station1 = row['station1']
            station2 = row['station2']
            distance = row['distance']

            # Add connections by retrieves the dictionary for station1, then accesses
            # the connections dictionary for station1. [station2] = travel_time adds
            # an entry for station2 with the travel time.

            # Travel time from station 1 to station 2, as well as the travel time
            # from station 2 to station 1
            stations[station1]['connections'][station2] = distance
            stations[station2]['connections'][station1] = distance
            connections.append({'station1': station1, 'station2': station2, 'distance': distance})

    return stations, connections

# Files
stations_file = 'StationsHolland.csv'
connections_file = 'ConnectiesHolland.csv'

# Read data function
stations, connections = read_data(stations_file, connections_file)

# pprint.pprint(stations)
#
# pprint.pprint(connections)
# print(stations['Alkmaar']['connections']['Castricum'])

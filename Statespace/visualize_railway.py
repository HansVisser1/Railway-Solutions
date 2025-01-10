import pandas as pd
import matplotlib.pyplot as plt
import csv

def import_stations(csv_file):
    df = pd.read_csv(csv_file, sep = ',')
    return(df)

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

            stations[station1]['connections'][station2] = distance
            stations[station2]['connections'][station1] = distance
            connections.append({'station1': station1, 'station2': station2, 'distance': distance})
    return stations, connections

def station_dict(dataframe):
    station_dict = dict(zip(dataframe['station'], zip(dataframe['x'], dataframe['y'])))
    return(station_dict)

def visualize_stations(station_dict):
    # creating the names and coordinate lists
    station_names = station_dict.keys()
    coordinate_list = list(station_dict.values())
    x_coordinates = list((coordinates[0] for coordinates in coordinate_list))
    y_coordinates = list((coordinates[1] for coordinates in coordinate_list))

    # plotting the station coordinates
    plt.figure(figsize = (10, 10))
    plt.scatter(x_coordinates, y_coordinates, color = 'blue', marker = 'o', label = 'stations', zorder = 1)

    # naming the stations at their coordinates
    for name, x, y in zip(station_names, x_coordinates, y_coordinates):
        plt.text(x, y, name, fontsize = 8, ha = 'right', color = 'black')

    # adding labels and title
    plt.xticks([])
    plt.yticks([])
    plt.title('Stations Noord-Holland')


def visualize_connections(station_dictionary):
    plotted_connections = []
    for station, station_data in station_dictionary.items():
        for destination in station_data['connections']:
            if (station, destination) not in plotted_connections and (destination, station) not in plotted_connections:
                x_coordinates = []
                y_coordinates = []
                x_coordinates.append(float(station_dictionary[station]['x']))
                x_coordinates.append(float(station_dictionary[destination]['x']))
                y_coordinates.append(float(station_dictionary[station]['y']))
                y_coordinates.append(float(station_dictionary[destination]['y']))

                # ensure connection appears once in legend
                if len(plotted_connections) == 0:
                    plt.plot(x_coordinates, y_coordinates, color = 'red', linestyle = '-', zorder = 0, label = 'connections')
                else:
                    plt.plot(x_coordinates, y_coordinates, color = 'red', linestyle = '-', zorder = 0)

                plotted_connections.append((station, destination))

    # plotting legend and showing figure
    plt.legend(loc = 'upper left')
    plt.show()
    print(plotted_connections)


if __name__ == "__main__":
    # creating a stations dataframe
    # Make sure the file path is correct after importing!
    df_stations = import_stations("../StationsHolland.csv")
    dict_stations, dict_connections = read_data('../StationsHolland.csv', '../ConnectiesHolland.csv')

    # creating dictionary of station coordinates
    station_coordinate_dict = station_dict(df_stations)

    # visualizing the stations, function order is important
    visualize_stations(station_coordinate_dict)
    visualize_connections(dict_stations)

import pandas as pd
import matplotlib.pyplot as plt
import csv

def visualize_stations(station_dict):
    """
    Function takes dictionary of stations produced by the read_data function,
    retrieves the station names and corresponding station coordinates from this dictionary
    and uses these to plot the stations in a matplotlib graph as points. The names of the stations
    are added in the graph next to the plotted station points. The function creates a plot but returns nothing.
    """
    # creating the names and coordinate lists
    x_coordinates = []
    y_coordinates = []
    station_names = station_dict.keys()

    # looping through dictionary to retrieve station coordinates
    for station in station_dict.keys():
        x_coordinates.append(float(station_dict[station]['x']))
        y_coordinates.append(float(station_dict[station]['y']))

    # plotting the stations using coordinate list
    plt.figure(figsize = (8, 8))
    plt.scatter(x_coordinates, y_coordinates, color = 'blue', marker = 'o', label = 'stations', zorder = 1)

    # naming the stations at their coordinates using name list
    for name, x, y in zip(station_names, x_coordinates, y_coordinates):
        plt.text(x, y, name, fontsize = 8, ha = 'right', color = 'black')

    # plotting labels and adding title
    plt.xticks([])
    plt.yticks([])
    plt.title('Stations Noord-Holland')


def visualize_connections(station_dictionary):
    """
    Function takes dictionary of stations produced by the read_data function,
    retrieves the station coordinates from this dictionary and plots the connections between the
    stations based on the listed connection in the dictionary and the coordinates corresponding to the
    connected stations. To ensure each connection is only plotted once, the plotted connections are placed in a set.
    The function plots the connections in the graph but returns nothing.
    """
    plotted_connections = [] #TODO CHANGE TO SET INSTEAD OF LIST
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
                    plt.plot(x_coordinates, y_coordinates, color = 'black', linestyle = '-', zorder = 0, label = 'connections')
                else:
                    plt.plot(x_coordinates, y_coordinates, color = 'black', linestyle = '-', zorder = 0)

                plotted_connections.append((station, destination))


def visualize_traject(station_dictionary, traject_list):
    traject_colours = ['gold', 'red', 'darkorange', 'lime', 'magenta', 'cyan', 'silver']

    for traject_number, traject in enumerate(traject_list):
        for connection_number, connection in enumerate(traject):
            station = connection[0]
            destination = connection[1]
            x_coordinates = []
            y_coordinates = []
            x_coordinates.append(float(station_dictionary[station]['x']))
            x_coordinates.append(float(station_dictionary[destination]['x']))
            y_coordinates.append(float(station_dictionary[station]['y']))
            y_coordinates.append(float(station_dictionary[destination]['y']))

            if connection_number == 0:
                plt.plot(x_coordinates, y_coordinates, color = traject_colours[traject_number],
                    label = f'traject {traject_number + 1}', linestyle = '--', zorder = 2)
                plt.legend(loc = 'upper left')
                plt.draw()
                plt.pause(0.5)

            else:
                plt.plot(x_coordinates, y_coordinates, color = traject_colours[traject_number],
                    linestyle = '--', zorder = 2)
                plt.legend(loc = 'upper left')
                plt.draw()
                plt.pause(0.25)
    plt.show()

def visualize_all_trajects(dict_stations, traject_list):
    """
    Function takes dictionary of stations produced by the read_data function and a traject list produced by
    the list_connections functions.
    Function combines all three visualize function for a complete visual product in the form of a matplotlib plot.
    The order of the visualize functions is of importance.
    """
    # callign the three functions
    visualize_stations(dict_stations)
    visualize_connections(dict_stations)
    visualize_traject(dict_stations, traject_list)

if __name__ == "__main__":
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

    # example of traject TODO REMOVE AFTERWARDS
    traject_short = [['Delft', 'Den Haag Centraal', '13'], ['Den Haag Centraal', 'Leiden Centraal','12'],
        ['Leiden Centraal', 'Den Haag Centraal', '12'], ['Den Haag Centraal', 'Leiden Centraal', '12'],
        ['Leiden Centraal', 'Heemstede-Aerdenhout', '13'], ['Heemstede-Aerdenhout', 'Haarlem', '6'],
        ['Haarlem', 'Amsterdam Sloterdijk', '11'], ['Amsterdam Sloterdijk', 'Haarlem', '11'],
        ['Haarlem', 'Beverwijk', '16'], ['Beverwijk', 'Castricum', '13']]

    traject_long = [[['Rotterdam Alexander', 'Rotterdam Centraal', '8'],
                      ['Rotterdam Centraal', 'Dordrecht', '17'],
                      ['Dordrecht', 'Rotterdam Centraal', '17'],
                      ['Rotterdam Centraal', 'Rotterdam Alexander', '8'],
                      ['Rotterdam Alexander', 'Rotterdam Centraal', '8'],
                      ['Rotterdam Centraal', 'Rotterdam Alexander', '8'],
                      ['Rotterdam Alexander', 'Gouda', '10'],
                      ['Gouda', 'Den Haag Centraal', '18'],
                      ['Den Haag Centraal', 'Gouda', '18']],
                     [['Zaandam', 'Amsterdam Sloterdijk', '6'],
                      ['Amsterdam Sloterdijk', 'Haarlem', '11'],
                      ['Haarlem', 'Amsterdam Sloterdijk', '11'],
                      ['Amsterdam Sloterdijk', 'Haarlem', '11'],
                      ['Haarlem', 'Amsterdam Sloterdijk', '11'],
                      ['Amsterdam Sloterdijk', 'Amsterdam Zuid', '16'],
                      ['Amsterdam Zuid', 'Schiphol Airport', '6'],
                      ['Schiphol Airport', 'Leiden Centraal', '15'],
                      ['Leiden Centraal', 'Heemstede-Aerdenhout', '13'],
                      ['Heemstede-Aerdenhout', 'Haarlem', '6'],
                      ['Haarlem', 'Amsterdam Sloterdijk', '11']]]

    # TODO Make sure the file path is correct after importing!
    dict_stations, dict_connections = read_data('../StationsHolland.csv', '../ConnectiesHolland.csv')

    # calling function of complete visual product
    visualize_all_trajects(dict_stations, traject_long)

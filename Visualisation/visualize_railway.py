import pandas as pd
import matplotlib.pyplot as plt
import csv
import geopandas as gpd

def visualize_area(plt_axis, province = True):
    """
    Function uses a GeoJSON file (not received as argument) and plots the outline of the area the trains will operate in.
    The argument plt_axis is the shared axis between all matplotlib plots/figures. Passing ensures plotting in the same figure.
    The province argument indicates if this is for the two provinces or for the entire country.

    GEOPANDAS NEEDS TO BE INSTALLED FOR THIS FUNCTION TO PROPERLY EXECUTE !
    terminal ---> pip install geopandas
    """
    # opening GeoJSON file
    geo_data = gpd.read_file("nl-all-provinces.geojson")
    plt_axis.set_xticks([])
    plt_axis.set_yticks([])

    # plotting the province borders
    if province:
        provinces = ["Noord-Holland", "Zuid-Holland"]
        province_geo_data = geo_data[geo_data["name"].isin(provinces)]
        province_geo_data.plot(ax = plt_axis, edgecolor = 'grey', facecolor = 'none', zorder = 0)
        plt_axis.set_title('Stations Noord- and Zuid-Holland')

    # plotting the country borders
    else:
        geo_data.plot(ax = plt_axis, edgecolor = 'grey', facecolor = 'none', zorder = 0)
        plt_axis.set_title('Stations Netherlands')

def visualize_stations(plt_axis, station_dict):
    """
    Function takes dictionary of stations produced by the read_data function,
    retrieves the station names and corresponding station coordinates from this dictionary
    and uses these to plot the stations in a matplotlib graph as points. The names of the stations
    are added in the graph next to the plotted station points. The function creates a plot but returns nothing.
    The argument plt_axis is the shared axis between all matplotlib plots/figures. Passing ensures plotting in the same figure.
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
    plt_axis.scatter(x_coordinates, y_coordinates, color = 'blue', marker = 'o', label = 'stations', zorder = 2)

    # naming the stations at their coordinates using name list
    va_dict = {'Alphen a/d Rijn': 'bottom','Den Helder': 'bottom', 'Gouda': 'bottom', 'Rotterdam Centraal': 'center',
                'Rotterdam Alexander': 'bottom', 'Schiphol Airport': 'top', 'Zaandam': 'center',
                'Amsterdam Centraal': 'center', 'Amsterdam Amstel': 'center', 'Amsterdam Zuid': 'top',
                'Amsterdam Sloterdijk': 'bottom', 'Heemstede-Aerdenhout': 'center'}
    ha_dict = {'Alphen a/d Rijn': 'left', 'Den Helder': 'left', 'Gouda': 'left', 'Rotterdam Centraal': 'left',
                'Rotterdam Alexander': 'left', 'Schiphol Airport': 'left', 'Zaandam': 'left',
                'Amsterdam Centraal': 'left', 'Amsterdam Amstel': 'left', 'Amsterdam Zuid': 'left',
                'Amsterdam Sloterdijk': 'left', 'Heemstede-Aerdenhout': 'right'}

    for name, x, y in zip(station_names, x_coordinates, y_coordinates):
        if name in va_dict or name in ha_dict:
            pass
            plt_axis.text(x, y, name, fontsize = 8, ha = ha_dict[name], va = va_dict[name], color = 'black')
        else:
            pass # TODO REMOVE
            plt_axis.text(x, y, name, fontsize = 8, ha = 'right', va = 'bottom', color = 'black')


def visualize_connections(plt_axis, station_dictionary):
    """
    Function takes dictionary of stations produced by the read_data function,
    retrieves the station coordinates from this dictionary and plots the connections between the
    stations based on the listed connection in the dictionary and the coordinates corresponding to the
    connected stations. To ensure each connection is only plotted once, the plotted connections are placed in a set.
    The argument plt_axis is the shared axis between all matplotlib plots/figures. Passing ensures plotting in the same figure.
    The function plots the connections in the graph but returns nothing.
    """
    # creating set to store plotted connections
    plotted_connections = set()

    # looping through dictionary to retrieve connection coordinates
    for station, station_data in station_dictionary.items():
        for destination in station_data['connections']:

            # checking if connection has already been plotted
            if (station, destination) not in plotted_connections and (destination, station) not in plotted_connections:

                # adding coordinates for connection between stations to lists
                x_coordinates = []
                y_coordinates = []
                x_coordinates.append(float(station_dictionary[station]['x']))
                x_coordinates.append(float(station_dictionary[destination]['x']))
                y_coordinates.append(float(station_dictionary[station]['y']))
                y_coordinates.append(float(station_dictionary[destination]['y']))

                # plotting connections and ensuring connection label appears only once in graph legend
                if len(plotted_connections) == 0:
                    plt_axis.plot(x_coordinates, y_coordinates, color = 'black', linestyle = '-', zorder = 1, label = 'connections')
                else:
                    plt_axis.plot(x_coordinates, y_coordinates, color = 'black', linestyle = '-', zorder = 1)

                # adding plotted connection to set of plotted connections
                plotted_connections.add((station, destination))


def visualize_traject(plt_axis, station_dictionary, traject_list):
    """
    Function takes dictionary of stations produced by the read_data function and a traject list produced by
    the list_connections function. It then plots every connection in the different trajects one by one and visualizes every step
    of the plotting in the graph. Each traject (and corresponding connections) gets its own colour in the plotted graph.
    The argument plt_axis is the shared axis between all matplotlib plots/figures. Passing ensures plotting in the same figure.
    This function plots the trajects in the fully visualized graph, and displays the graph, but returns nothing.
    """
    # creating list of different colours for the trajects to be plotted in
    # TODO ADD ADDITIONAL COLOURS FOR 20 TRAJECTS LATER ON
    traject_colours = ['gold', 'red', 'darkorange', 'lime', 'magenta', 'cyan', 'silver']

    # looping through the list of trajects and connections therein
    for traject_number, traject in enumerate(traject_list):
        for connection_number, connection in enumerate(traject):

            # defining stations and adding coordinates to seperate lists
            station = connection[0]
            destination = connection[1]
            x_coordinates = []
            y_coordinates = []
            x_coordinates.append(float(station_dictionary[station]['x']))
            x_coordinates.append(float(station_dictionary[destination]['x']))
            y_coordinates.append(float(station_dictionary[station]['y']))
            y_coordinates.append(float(station_dictionary[destination]['y']))

            # plotting traject connections and ensuring traject label appears only once in graph legend
            if connection_number == 0:
                plt_axis.plot(x_coordinates, y_coordinates, color = traject_colours[traject_number],
                    label = f'traject {traject_number + 1}', linestyle = '--', zorder = 3)
                plt_axis.legend(loc = 'upper left')
                plt.draw()
                plt.pause(0.25)
            else:
                plt_axis.plot(x_coordinates, y_coordinates, color = traject_colours[traject_number],
                    linestyle = '--', zorder = 3)
                plt_axis.legend(loc = 'upper left')
                plt.draw()
                plt.pause(0.25)


def visualize_all_trajects(dict_stations, traject_list, province = True):
    """
    Function takes dictionary of stations produced by the read_data function and a traject list produced by
    the list_connections function.
    Function combines all three visualize functions for a complete visual product in the form of a matplotlib graph.
    The order of the visualize functions is of importance.
    """
    # defining figure and figure axis
    fig, plt_axis = plt.subplots(figsize=(8, 8))

    # calling the three visualisation functions
    visualize_area(plt_axis, province)
    visualize_stations(plt_axis, dict_stations)
    visualize_connections(plt_axis, dict_stations)
    visualize_traject(plt_axis, dict_stations, traject_list)

    # displaying the full final visual/graph
    plt.show()


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
    dict_stations_holland, dict_connections_holland = read_data('../StationsHolland.csv', '../ConnectiesHolland.csv')
    dict_stations_nl, dict_connections_nl = read_data('../StationsNationaal.csv', '../ConnectiesNationaal.csv')

    # calling function of complete visual product
    # visualize_all_trajects(dict_stations_holland, traject_long, province = True)
    visualize_all_trajects(dict_stations_nl, traject_long, province = False)

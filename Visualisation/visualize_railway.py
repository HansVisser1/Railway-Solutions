import pandas as pd
import matplotlib.pyplot as plt
import csv
import geopandas as gpd

def visualize_area(plt_axis, province, algorithm):
    """
    Function uses a GeoJSON file (not received as argument) and plots the outline of the area the trains will operate in.
    The argument plt_axis is the shared axis between all matplotlib plots/figures. Passing ensures plotting in the same figure.
    The province argument indicates if this is for the two provinces or for the entire country. The algorithm argument is
    the name of the algorithm that produced the to be visualed answer, and is used to plot the correct figure title.
    """
    # opening GeoJSON file
    # TODO change to Data/nl-all-provinces.geojson
    geo_data = gpd.read_file("nl-all-provinces.geojson")
    plt_axis.set_xticks([])
    plt_axis.set_yticks([])

    # plotting the province borders
    if province:
        provinces = ["Noord-Holland", "Zuid-Holland"]
        province_geo_data = geo_data[geo_data["name"].isin(provinces)]
        province_geo_data.boundary.plot(ax = plt_axis, edgecolor = 'grey', alpha = 1, zorder = 0)
        province_geo_data.plot(ax = plt_axis, facecolor = 'yellow', alpha = 0.1, zorder = 0)
        plt_axis.set_title(f'Stations Noord- and Zuid-Holland ({algorithm})')

    # plotting the country borders
    else:
        geo_data.boundary.plot(ax = plt_axis, edgecolor = 'grey', alpha = 1, zorder = 0)
        geo_data.plot(ax = plt_axis, facecolor = 'yellow', alpha = 0.1, zorder = 0)
        plt_axis.set_title(f'Stations Netherlands ({algorithm})')

def visualize_stations(plt_axis, station_dict, province):
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

    if province:
        # vertical and horizontal name placement dictionary for province(s)
        va_dict = {'Alphen a/d Rijn': 'bottom','Den Helder': 'bottom', 'Gouda': 'bottom', 'Rotterdam Centraal': 'center',
                    'Rotterdam Alexander': 'bottom', 'Schiphol Airport': 'top', 'Zaandam': 'center',
                    'Amsterdam Centraal': 'center', 'Amsterdam Amstel': 'center', 'Amsterdam Zuid': 'top',
                    'Amsterdam Sloterdijk': 'bottom', 'Heemstede-Aerdenhout': 'center'}
        ha_dict = {'Alphen a/d Rijn': 'left', 'Den Helder': 'left', 'Gouda': 'left', 'Rotterdam Centraal': 'left',
                    'Rotterdam Alexander': 'left', 'Schiphol Airport': 'left', 'Zaandam': 'left',
                    'Amsterdam Centraal': 'left', 'Amsterdam Amstel': 'left', 'Amsterdam Zuid': 'left',
                    'Amsterdam Sloterdijk': 'left', 'Heemstede-Aerdenhout': 'right'}
    else:
        # vertical and horizontal name placement dictionary for whole country
        va_dict = {'Leeuwarden': 'bottom', 'Groningen': 'bottom', 'Heerenveen': 'top', 'Zwolle': 'bottom',
                    'Vlissingen': 'top', 'Maastricht': 'top', 'Venlo': 'bottom', 's-Hertogenbosch': 'center',
                    'Den Helder': 'top', 'Den Haag Centraal': 'bottom', 'Enschede': 'top', 'Rotterdam Centraal': 'top',
                    'Roosendaal': 'top'}
        ha_dict = {'Leeuwarden': 'right', 'Groningen': 'left', 'Heerenveen': 'right', 'Zwolle': 'right',
                    'Vlissingen': 'right','Maastricht': 'right', 'Venlo': 'left', 's-Hertogenbosch': 'left',
                    'Den Helder': 'right', 'Den Haag Centraal': 'right', 'Enschede': 'left', 'Rotterdam Centraal': 'right',
                    'Roosendaal': 'left'}

    # naming the stations at their coordinates using name list
    for name, x, y in zip(station_names, x_coordinates, y_coordinates):
        if name in va_dict or name in ha_dict:
            if not province:
                plt_axis.text(x, y, name, fontsize = 9, ha = ha_dict[name], va = va_dict[name], color = 'black', weight = 'bold')
            else:
                plt_axis.text(x, y, name, fontsize = 9, ha = ha_dict[name], va = va_dict[name], color = 'black')

        elif name not in va_dict and not province:
            pass
        else:
            plt_axis.text(x, y, name, fontsize = 9, ha = 'right', va = 'bottom', color = 'black')

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

    # list of different colours for the trajects to be plotted in
    traject_colours = ['gold', 'red', 'darkorange', 'lime', 'magenta', 'cyan', 'silver', 'dodgerblue', 'yellowgreen',
                        'pink', 'mediumorchid', 'lightcoral', 'saddlebrown', 'deepskyblue',  'deeppink',
                        'olive', 'peru', 'mistyrose', 'mediumaquamarine',  'lightsteelblue']

    traject_colours_short = ['red', 'darkorange', 'lime', 'magenta', 'cyan', 'silver']

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
                plt_axis.plot(x_coordinates, y_coordinates, color = traject_colours_short[traject_number% len(traject_colours_short)],
                    label = f'traject {traject_number + 1}', linestyle = '--', zorder = 3)
                plt_axis.legend(loc = 'upper left')
                plt.draw()
                plt.pause(0.10)
            else:
                plt_axis.plot(x_coordinates, y_coordinates, color = traject_colours_short[traject_number % len(traject_colours_short)],
                    linestyle = '--', zorder = 3)
                plt_axis.legend(loc = 'upper left')
                plt.draw()
                plt.pause(0.10)


def visualize_all_trajects(dict_stations, traject_list, file_name = None, province = True, save_figure = False, algorithm = 'Test'):
    """
    Function takes dictionary of stations produced by the read_data function and a traject list produced by
    the list_connections function.
    Function combines all three visualize functions for a complete visual product in the form of a matplotlib graph.
    The order of the visualize functions is of importance.
    The arguments file_name, save_figure and algorithm are for plotting and saving the visualisation. To save the figure,
    a file name has to be given, save_figure set to True and an algorithm name can be added to plot it in the figure title.
    """
    # defining figure and figure axis
    fig, plt_axis = plt.subplots(figsize=(10, 10))

    # calling the three visualisation functions
    visualize_area(plt_axis, province, algorithm)
    visualize_stations(plt_axis, dict_stations, province)
    visualize_connections(plt_axis, dict_stations)
    visualize_traject(plt_axis, dict_stations, traject_list)

    if save_figure:
        # saving figure as png image
        plt.savefig(file_name, dpi = 600, bbox_inches = 'tight')

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
    traject_empty = []

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

    traject_depthfirst = [[['Dordrecht', 'Rotterdam Centraal', 0], ['Rotterdam Centraal', 'Schiedam Centrum', 0],
        ['Schiedam Centrum', 'Delft', 0], ['Delft', 'Den Haag Centraal', 0], ['Den Haag Centraal', 'Leiden Centraal', 0],
        ['Leiden Centraal', 'Heemstede-Aerdenhout', 0], ['Heemstede-Aerdenhout', 'Haarlem', 0], ['Haarlem', 'Amsterdam Sloterdijk', 0],
        ['Amsterdam Sloterdijk', 'Amsterdam Centraal', 0], ['Amsterdam Centraal', 'Amsterdam Amstel', 0], ['Amsterdam Amstel', 'Amsterdam Zuid', 0],
        ['Amsterdam Zuid', 'Schiphol Airport', 0], ['Schiphol Airport', 'Amsterdam Zuid', 0]], [['Zaandam', 'Beverwijk', 0], ['Beverwijk', 'Castricum', 0],
        ['Castricum', 'Zaandam', 0], ['Zaandam', 'Beverwijk', 0], ['Beverwijk', 'Castricum', 0], ['Castricum', 'Alkmaar', 0], ['Alkmaar', 'Castricum', 0],
        ['Castricum', 'Zaandam', 0]], [['Rotterdam Alexander', 'Gouda', 0], ['Gouda', 'Alphen a/d Rijn', 0], ['Alphen a/d Rijn', 'Leiden Centraal', 0],
        ['Leiden Centraal', 'Schiphol Airport', 0], ['Schiphol Airport', 'Amsterdam Zuid', 0], ['Amsterdam Zuid', 'Amsterdam Sloterdijk', 0],
        ['Amsterdam Sloterdijk', 'Zaandam', 0], ['Zaandam', 'Hoorn', 0]], [['Den Helder', 'Alkmaar', 0], ['Alkmaar', 'Hoorn', 0], ['Hoorn', 'Zaandam', 0],
        ['Zaandam', 'Amsterdam Sloterdijk', 0], ['Amsterdam Sloterdijk', 'Haarlem', 0], ['Haarlem', 'Beverwijk', 0]],
        [['Schiphol Airport', 'Leiden Centraal', 0], ['Leiden Centraal', 'Den Haag Centraal', 0], ['Den Haag Centraal', 'Gouda', 0],
        ['Gouda', 'Rotterdam Alexander', 0], ['Rotterdam Alexander', 'Rotterdam Centraal', 0], ['Rotterdam Centraal', 'Schiedam Centrum', 0],
        ['Schiedam Centrum', 'Delft', 0], ['Delft', 'Den Haag Centraal', 0], ['Den Haag Centraal', 'Gouda', 0]]]

    traject_random = [[['Rotterdam Alexander', 'Rotterdam Centraal', '8'], ['Rotterdam Centraal', 'Dordrecht', '17'],
        ['Dordrecht', 'Rotterdam Centraal', '17'], ['Rotterdam Centraal', 'Rotterdam Alexander', '8'],
        ['Rotterdam Alexander', 'Rotterdam Centraal', '8'], ['Rotterdam Centraal', 'Schiedam Centrum', '5'], ['Schiedam Centrum', 'Delft', '7'],
        ['Delft', 'Den Haag Centraal', '13'], ['Den Haag Centraal', 'Leiden Centraal', '12'], ['Leiden Centraal', 'Den Haag Centraal', '12'],
        ['Den Haag Centraal', 'Leiden Centraal', '12']], [['Zaandam', 'Castricum', '12'], ['Castricum', 'Zaandam', '12'], ['Zaandam', 'Hoorn', '26'],
        ['Hoorn', 'Zaandam', '26'], ['Zaandam', 'Hoorn', '26']], [['Rotterdam Centraal', 'Schiedam Centrum', '5'],
        ['Schiedam Centrum', 'Rotterdam Centraal', '5'], ['Rotterdam Centraal', 'Rotterdam Alexander', '8'], ['Rotterdam Alexander', 'Gouda', '10'],
        ['Gouda', 'Den Haag Centraal', '18'], ['Den Haag Centraal', 'Gouda', '18'], ['Gouda', 'Alphen a/d Rijn', '19'], ['Alphen a/d Rijn', 'Gouda', '19'],
        ['Gouda', 'Den Haag Centraal', '18']], [['Castricum', 'Beverwijk', '13'], ['Beverwijk', 'Zaandam', '25'], ['Zaandam', 'Beverwijk', '25'],
        ['Beverwijk', 'Castricum', '13'], ['Castricum', 'Alkmaar', '9'], ['Alkmaar', 'Castricum', '9'], ['Castricum', 'Zaandam','12'],
        ['Zaandam', 'Castricum', '12']], [['Den Helder', 'Alkmaar', '36'], ['Alkmaar', 'Castricum', '9'], ['Castricum', 'Beverwijk', '13'],
        ['Beverwijk', 'Castricum', '13'], ['Castricum', 'Alkmaar', '9'], ['Alkmaar', 'Castricum', '9'], ['Castricum', 'Zaandam', '12'],
        ['Zaandam', 'Castricum', '12']]]

    traject_greedy = [[['Den Helder', 'Alkmaar', 36], ['Alkmaar', 'Castricum', 9], ['Castricum', 'Zaandam', 12], ['Zaandam', 'Amsterdam Sloterdijk', 6],
        ['Amsterdam Sloterdijk', 'Amsterdam Centraal', 6], ['Amsterdam Centraal', 'Amsterdam Amstel', 8], ['Amsterdam Amstel', 'Amsterdam Zuid', 10],
        ['Amsterdam Zuid', 'Schiphol Airport', 6], ['Schiphol Airport', 'Leiden Centraal', 15], ['Leiden Centraal', 'Den Haag Centraal', 12]],
        [['Dordrecht', 'Rotterdam Centraal', 17], ['Rotterdam Centraal', 'Schiedam Centrum', 5], ['Schiedam Centrum', 'Delft', 7],
        ['Delft', 'Den Haag Centraal', 13], ['Den Haag Centraal', 'Leiden Centraal', 12], ['Leiden Centraal', 'Heemstede-Aerdenhout', 13],
        ['Heemstede-Aerdenhout', 'Haarlem', 6], ['Haarlem', 'Amsterdam Sloterdijk', 11], ['Amsterdam Sloterdijk', 'Amsterdam Centraal', 6],
        ['Amsterdam Centraal', 'Amsterdam Amstel', 8], ['Amsterdam Amstel', 'Amsterdam Zuid', 10], ['Amsterdam Zuid', 'Schiphol Airport', 6],
        ['Schiphol Airport', 'Amsterdam Zuid', 6]], [['Dordrecht', 'Rotterdam Centraal', 17], ['Rotterdam Centraal', 'Schiedam Centrum', 5],
        ['Schiedam Centrum', 'Delft', 7], ['Delft', 'Den Haag Centraal', 13], ['Den Haag Centraal', 'Leiden Centraal', 12],
        ['Leiden Centraal', 'Heemstede-Aerdenhout', 13], ['Heemstede-Aerdenhout', 'Haarlem', 6], ['Haarlem', 'Amsterdam Sloterdijk', 11],
        ['Amsterdam Sloterdijk', 'Amsterdam Centraal', 6], ['Amsterdam Centraal', 'Amsterdam Amstel', 8], ['Amsterdam Amstel', 'Amsterdam Zuid', 10],
        ['Amsterdam Zuid', 'Schiphol Airport', 6], ['Schiphol Airport', 'Amsterdam Zuid', 6]], [['Amsterdam Centraal', 'Amsterdam Sloterdijk', 6],
        ['Amsterdam Sloterdijk', 'Zaandam', 6], ['Zaandam', 'Castricum', 12], ['Castricum', 'Alkmaar', 9], ['Alkmaar', 'Hoorn', 24],
        ['Hoorn', 'Zaandam', 26], ['Zaandam', 'Amsterdam Sloterdijk', 6], ['Amsterdam Sloterdijk', 'Amsterdam Centraal', 6],
        ['Amsterdam Centraal', 'Amsterdam Amstel', 8], ['Amsterdam Amstel', 'Amsterdam Zuid', 10], ['Amsterdam Zuid', 'Schiphol Airport', 6]],
        [['Amsterdam Sloterdijk', 'Amsterdam Centraal', 6], ['Amsterdam Centraal', 'Amsterdam Amstel', 8], ['Amsterdam Amstel', 'Amsterdam Zuid', 10],
        ['Amsterdam Zuid', 'Schiphol Airport', 6], ['Schiphol Airport', 'Leiden Centraal', 15], ['Leiden Centraal', 'Den Haag Centraal', 12],
        ['Den Haag Centraal', 'Delft', 13], ['Delft', 'Schiedam Centrum', 7], ['Schiedam Centrum', 'Rotterdam Centraal', 5],
        ['Rotterdam Centraal', 'Rotterdam Alexander', 8], ['Rotterdam Alexander', 'Gouda', 10], ['Gouda', 'Den Haag Centraal', 18]]]

    traject_best_result = [[
        ['Alkmaar', 'Castricum', 0],
        ['Castricum', 'Zaandam', 0],
        ['Zaandam', 'Amsterdam Sloterdijk', 0],
        ['Amsterdam Sloterdijk', 'Amsterdam Centraal', 0],
        ['Amsterdam Centraal', 'Amsterdam Amstel', 0],
        ['Amsterdam Amstel', 'Amsterdam Zuid', 0],
        ['Amsterdam Zuid', 'Schiphol Airport', 0],
        ['Schiphol Airport', 'Leiden Centraal', 0],
        ['Leiden Centraal', 'Den Haag Laan v NOI', 0],
        ['Den Haag Laan v NOI', 'Delft', 0],
        ['Delft', 'Schiedam Centrum', 0],
        ['Schiedam Centrum', 'Rotterdam Centraal', 0],
        ['Rotterdam Centraal', 'Rotterdam Alexander', 0],
        ['Rotterdam Alexander', 'Rotterdam Blaak', 0],
        ['Rotterdam Blaak', 'Schiedam Centrum', 0],
        ['Schiedam Centrum', 'Rotterdam Centraal', 0],
        ['Rotterdam Centraal', 'Rotterdam Alexander', 0],
        ['Rotterdam Alexander', 'Rotterdam Blaak', 0],
        ['Rotterdam Blaak', 'Schiedam Centrum', 0],
        ['Schiedam Centrum', 'Delft', 0],
        ['Delft', 'Schiedam Centrum', 0]],[
        ['Sittard', 'Roermond', 0],
        ['Roermond', 'Weert', 0],
        ['Weert', 'Eindhoven', 0],
        ['Eindhoven', 'Tilburg', 0],
        ['Tilburg', 's-Hertogenbosch', 0],
        ['s-Hertogenbosch', 'Oss', 0],
        ['Oss', 'Nijmegen', 0],
        ['Nijmegen', 'Arnhem Centraal', 0],
        ['Arnhem Centraal', 'Dieren', 0],
        ['Dieren', 'Zutphen', 0],
        ['Zutphen', 'Deventer', 0],
        ['Deventer', 'Apeldoorn', 0],
        ['Apeldoorn', 'Deventer', 0]],
        [['s-Hertogenbosch', 'Tilburg', 0],
        ['Tilburg', 'Breda', 0],
        ['Breda', 'Dordrecht', 0],
        ['Dordrecht', 'Rotterdam Blaak', 0],
        ['Rotterdam Blaak', 'Rotterdam Alexander', 0],
        ['Rotterdam Alexander', 'Gouda', 0],
        ['Gouda', 'Den Haag Centraal', 0],
        ['Den Haag Centraal', 'Leiden Centraal', 0],
        ['Leiden Centraal', 'Den Haag HS', 0],
        ['Den Haag HS', 'Delft', 0],
        ['Delft', 'Den Haag Centraal', 0],
        ['Den Haag Centraal', 'Leiden Centraal', 0],
        ['Leiden Centraal', 'Heemstede-Aerdenhout', 0],
        ['Heemstede-Aerdenhout', 'Haarlem', 0],
        ['Haarlem', 'Heemstede-Aerdenhout', 0]],[
        ['Amsterdam Centraal', 'Utrecht Centraal', 0],
        ['Utrecht Centraal', 'Amersfoort', 0],
        ['Amersfoort', 'Zwolle', 0],
        ['Zwolle', 'Deventer', 0],
        ['Deventer', 'Almelo', 0],
        ['Almelo', 'Hengelo', 0],
        ['Hengelo', 'Enschede', 0],
        ['Enschede', 'Hengelo', 0],
        ['Hengelo', 'Almelo', 0],
        ['Almelo', 'Hengelo', 0],
        ['Hengelo', 'Enschede', 0]],
        [['Heerenveen', 'Leeuwarden', 0],
        ['Leeuwarden', 'Groningen', 0],
        ['Groningen', 'Assen', 0],
        ['Assen', 'Zwolle', 0],
        ['Zwolle', 'Steenwijk', 0],
        ['Steenwijk', 'Heerenveen', 0],
        ['Heerenveen', 'Leeuwarden', 0],
        ['Leeuwarden', 'Heerenveen', 0]],
        [['Lelystad Centrum', 'Almere Centrum', 0],
        ['Almere Centrum', 'Hilversum', 0],
        ['Hilversum', 'Utrecht Centraal', 0],
        ['Utrecht Centraal', 'Gouda', 0],
        ['Gouda', 'Den Haag HS', 0],
        ['Den Haag HS', 'Delft', 0],
        ['Delft', 'Schiedam Centrum', 0],
        ['Schiedam Centrum', 'Rotterdam Centraal', 0],
        ['Rotterdam Centraal', 'Dordrecht', 0],
        ['Dordrecht', 'Roosendaal', 0],
        ['Roosendaal', 'Etten-Leur', 0],
        ['Etten-Leur', 'Breda', 0],
        ['Breda', 'Etten-Leur', 0]],
        [['Helmond', 'Eindhoven', 0],
        ['Eindhoven', 'Weert', 0],
        ['Weert', 'Roermond', 0],
        ['Roermond', 'Sittard', 0],
        ['Sittard', 'Heerlen', 0],
        ['Heerlen', 'Sittard', 0],
        ['Sittard', 'Maastricht', 0],
        ['Maastricht', 'Sittard', 0],
        ['Sittard', 'Heerlen', 0],
        ['Heerlen', 'Sittard', 0],
        ['Sittard', 'Maastricht', 0],
        ['Maastricht', 'Sittard', 0]],
        [['Venlo', 'Helmond', 0],
        ['Helmond', 'Eindhoven', 0],
        ['Eindhoven', 's-Hertogenbosch', 0],
        ['s-Hertogenbosch', 'Utrecht Centraal', 0],
        ['Utrecht Centraal', 'Schiphol Airport', 0],
        ['Schiphol Airport', 'Amsterdam Zuid', 0],
        ['Amsterdam Zuid', 'Amsterdam Sloterdijk', 0],
        ['Amsterdam Sloterdijk', 'Haarlem', 0],
        ['Haarlem', 'Beverwijk', 0],
        ['Beverwijk', 'Castricum', 0]],
        [['Gouda', 'Alphen a/d Rijn', 0],
        ['Alphen a/d Rijn', 'Utrecht Centraal', 0],
        ['Utrecht Centraal', 'Amsterdam Amstel', 0],
        ['Amsterdam Amstel', 'Amsterdam Centraal', 0],
        ['Amsterdam Centraal', 'Almere Centrum', 0],
        ['Almere Centrum', 'Amsterdam Amstel', 0],
        ['Amsterdam Amstel', 'Utrecht Centraal', 0],
        ['Utrecht Centraal', 'Ede-Wageningen', 0],
        ['Ede-Wageningen', 'Arnhem Centraal', 0]],
        [['Zutphen', 'Apeldoorn', 0],
        ['Apeldoorn', 'Deventer', 0],
        ['Deventer', 'Zutphen', 0],
        ['Zutphen', 'Apeldoorn', 0],
        ['Apeldoorn', 'Deventer', 0],
        ['Deventer', 'Zutphen', 0],
        ['Zutphen', 'Apeldoorn', 0],
        ['Apeldoorn', 'Deventer', 0],
        ['Deventer', 'Zutphen', 0],
        ['Zutphen', 'Apeldoorn', 0],
        ['Apeldoorn', 'Amersfoort', 0]]]

    # TODO Make sure the file path is correct after importing!
    dict_stations_holland, dict_connections_holland = read_data('../StationsHolland.csv', '../ConnectiesHolland.csv')
    dict_stations_nl, dict_connections_nl = read_data('../StationsNationaal.csv', '../ConnectiesNationaal.csv')

    # # calling function of complete visual product
    # visualize_all_trajects(dict_stations_holland, traject_long, province = True)
    # visualize_all_trajects(dict_stations_nl, traject_best_result, province = False)
    visualize_all_trajects(dict_stations_holland, traject_empty, province = True, save_figure = True,
                            file_name = 'empty_map.png', algorithm = 'Empty')

    # exit () prevents last block from executing
    exit()

    visualize_all_trajects(dict_stations_holland, traject_depthfirst, province = True, save_figure = True,
                            file_name = 'visualisation_depthfirst_v2.png', algorithm = 'DepthFirst')
    visualize_all_trajects(dict_stations_holland, traject_random, province = True, save_figure = True,
                            file_name = 'visualisation_random_v2.png', algorithm = 'Random')
    visualize_all_trajects(dict_stations_holland, traject_greedy, province = True, save_figure = True,
                            file_name = 'visualisation_greedy_v2.png', algorithm = 'Greedy')



    # code block for counting connections in dictionary
    count_connection_1 = set()
    for connection in dict_connections_holland:
        if connection.values() not in count_connection_1:
            count_connection_1.add(tuple(connection.values()))

    total_time_1 = 0
    for connection in count_connection_1:
        total_time_1 += float(connection[2])
    print(f"Total time for Noord- and Zuid-Holland is {total_time_1}")

    count_connection_2 = set()
    for connection in dict_connections_nl:
        if connection.values() not in count_connection_2:
            count_connection_2.add(tuple(connection.values()))

    total_time_2 = 0
    for connection in count_connection_2:
        total_time_2 += float(connection[2])
    print(f"Total time for Netherlands is {total_time_2}")

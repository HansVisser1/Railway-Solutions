import pandas as pd
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import csv
import geopandas as gpd
import numpy as np

def visualize_area(plt_axis, province, algorithm):
    """
    Function uses a GeoJSON file (not received as argument) and plots the outline of the area the trains will operate in.
    The argument plt_axis is the shared axis between all matplotlib plots/figures. Passing ensures plotting in the same figure.
    The province argument indicates if this is for the two provinces or for the entire country. The algorithm argument is
    the name of the algorithm that produced the to be visualed answer, and is used to plot the correct figure title.
    """
    # opening GeoJSON file
    geo_data = gpd.read_file("Data/nl-all-provinces.geojson")
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


def visualize_traject(plt_axis, station_dictionary, traject_list, save_gif, gif_name):
    """
    Function takes dictionary of stations produced by the read_data function and a traject list produced by
    the list_connections function. It then plots every connection in the different trajects one by one and visualizes every step
    of the plotting in the graph. Each traject (and corresponding connections) gets its own colour in the plotted graph.
    The argument plt_axis is the shared axis between all matplotlib plots/figures. Passing ensures plotting in the same figure.
    If the save_gif argument is set to True, a GIF of the visualisation will be produced.
    This function plots the trajects in the fully visualized graph, creates a GIF and displays the graph, but returns nothing.
    """
    # list of different colours for the trajects to be plotted in
    traject_colours = ['gold', 'red', 'darkorange', 'lime', 'magenta', 'cyan', 'silver', 'dodgerblue', 'yellowgreen',
                        'pink', 'mediumorchid', 'lightcoral', 'saddlebrown', 'deepskyblue',  'deeppink',
                        'olive', 'peru', 'mistyrose', 'mediumaquamarine',  'lightsteelblue']
    gif_frames = []

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
            else:
                plt_axis.plot(x_coordinates, y_coordinates, color = traject_colours[traject_number],
                    linestyle = '--', zorder = 3)
                plt_axis.legend(loc = 'upper left')

            # drawing and displaying figure
            plt.draw()
            plt.pause(0.10)

            # capturing frames for GIF and storing them
            plt_axis.figure.canvas.draw()
            frame = np.array(plt_axis.figure.canvas.renderer.buffer_rgba())
            plt.tight_layout(pad=0.1)
            gif_frames.append(frame)

    if save_gif:
        # saving the GIF
        imageio.mimsave(gif_name, gif_frames, duration=0.1, loop=0)

def visualize_all_trajects(dict_stations, traject_list, file_name = None, province = True, save_figure = False, algorithm = 'Test', save_gif = False):
    """
    Function takes dictionary of stations produced by the read_data function and a traject list produced by
    the list_connections function.
    Function combines all three visualize functions for a complete visual product in the form of a matplotlib graph.
    The order of the visualize functions is of importance.
    The arguments file_name, save_figure and algorithm are for plotting and saving the visualisation. To save the figure,
    a file name has to be given, save_figure set to True and an algorithm name can be added to plot it in the figure title.
    If the visualisation needs to be saved as a GIF as well, the save_gif argument needs to be set to True.
    """
    # defining file_names
    if file_name:
        png_name = file_name + '.png'
        gif_name = file_name + '_GIF.gif'
    else:
        png_name = None
        gif_name = None

    # defining figure and figure axis
    fig, plt_axis = plt.subplots(figsize=(10, 10))

    # calling the three visualisation functions
    visualize_area(plt_axis, province, algorithm)
    visualize_stations(plt_axis, dict_stations, province)
    visualize_connections(plt_axis, dict_stations)
    visualize_traject(plt_axis, dict_stations, traject_list, save_gif, gif_name)

    if save_figure:
        # saving figure as png image
        plt.savefig(png_name, dpi = 600, bbox_inches = 'tight')

    # displaying the full final visual/graph
    plt.show()

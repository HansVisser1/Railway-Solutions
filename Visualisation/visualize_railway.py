import pandas as pd
import matplotlib.pyplot as plt

def import_stations(csv_file):
    df = pd.read_csv(csv_file, sep = ',')
    return(df)

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
    plt.scatter(x_coordinates, y_coordinates, color = 'blue', marker = 'o', label = 'stations')

    # naming the stations at their coordinates
    for name, x, y in zip(station_names, x_coordinates, y_coordinates):
        plt.text(x, y, name, fontsize = 8, ha = 'right', color = 'black')

    # adding labels and title
    plt.xticks([])
    plt.yticks([])
    plt.title('Stations Noord-Holland')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Execute functions
    df_stations = import_stations('StationsHolland.csv')

    station_coordinate_dict = station_dict(df_stations)

    visualize_stations(station_coordinate_dict)

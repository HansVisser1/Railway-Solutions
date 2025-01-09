import random
from read_files import read_data

class Station():
    def __init__(self, name, x_coord, y_coord):
        """
        This method stores the name and coordinates of the station in the station object.
        """
        self.name = name
        self.x = x_coord
        self.y = y_coord

class Connection():
    def __init__(self, time, station1):
        """
        This method stores the duration and the connected stations in the connection object.
        """
        self.time = time
        self.stations = [station2.name]

    def add_time_and_station(self, time, station):


class Traject():
    def __init__(self):
        """
        The init method initializes a route list, which is kept empty, a time value which is set to None and
        the method stores the connections_list in the Traject object.
        """
        self.stations = []
        self.connections = []
        self.available_connections = []
        self.time = None
        self.max_time = 120
        self.time_condition = False
        self.current_station = None
        self.connections_dict = {}

    def run(self, dictionary):



    def starting_station(self, station):
        self.current_station = station
        self.stations.append(station)

    def determine_available_connections(self, connections_dict):
        """
        This methods adds connections from a list to the Traject object as long as they don't exceed the maximum time.
        It also checks whether the station can be connected.
        """
        self.connections_dict = connections_dict[current_station]
        self.available_connections = []

        for key in connections[self.current_station]['connections'].keys():
            if duration() + connections[self.current_station]['connections'][key] =< self.max_time:
                self.available_connections.append(key)

    def add_connection(self):
        next_station = random.sample(self.available_connections)
        self.connections.append([self.current_station, next_station, self.connections_dict[next_station]])
        if next_station not in self.stations:
            self.stations.append(next_station)

    def duration(self):
        """
        This method calculates the duration of the Traject
        """
        self.time = 0
        for connection in self.connections:
            self.time += connection.time
        return self.time

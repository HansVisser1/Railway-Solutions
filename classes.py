import random
import pprint
from read_files import read_data

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

    def run(self, stations_path, connections_path):
        stations_dict, connections_list = read_data(stations_path, connections_path)

        stations = []
        for station in stations_dict.keys():
            stations.append(station)
        start_station = (random.sample(stations, 1)[0])

        print(start_station)
        self.starting_station(start_station)

        self.determine_available_connections(stations_dict)
        print(self.available_connections)

    def starting_station(self, station):
        self.current_station = station
        self.stations.append(station)

    def determine_available_connections(self, stations_dict):
        """
        This methods adds connections from a list to the Traject object as long as they don't exceed the maximum time.
        It also checks whether the station can be connected.
        """
        connections_dict = stations_dict[self.current_station]
        self.available_connections = []

        for key in connections_dict['connections'].keys():
            if self.duration() + int(connections_dict['connections'][key]) <= self.max_time:
                self.available_connections.append(key)

    def add_connection(self):
        next_station = random.sample(self.available_connections)
        self.connections.append([self.current_station, next_station, self.connections_dict[next_station]])
        if next_station not in self.stations:
            self.stations.append(next_station)
        self.current_station = next_station

    def duration(self):
        """
        This method calculates the duration of the Traject
        """
        self.time = 0
        for connection in self.connections:
            self.time += connection.time
        return self.time

traject1 = Traject()
traject1.run('StationsHolland.csv', 'ConnectiesHolland.csv')

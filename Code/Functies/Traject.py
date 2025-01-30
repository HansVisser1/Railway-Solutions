import random
import pprint
from Code.Functies.read_files import read_data

class Traject():
    def __init__(self):
        """
        The init method initializes a route list, which is kept empty, a time value which is set to None and
        the method stores the connections_list in the Traject object.
        """
        self.stations = []
        self.connections = []
        self.available_connections = []
        self.time = 0
        self.max_time = 120
        self.time_condition = False
        self.current_station = None
        self.connections_dict = {}
        self.stations_path = None
        self.connections_path = None
        self.stations_dict = None

    def run(self, stations_path, connections_path):
        """
        This method runs all the functions which are required to make a trajectory.
        """
        self.stations_path = stations_path
        self.connections_path = connections_path
        self.stations_dict, connections_dict = read_data(stations_path, connections_path)

    def determine_available_connections(self, stations_dict):
        """
        This method determines the available connections at the current station of the traject, and stores these in a self variable as a list.
        """
        # dictionary with the information of the current station
        self.connections_dict = stations_dict[self.current_station]
        self.available_connections = []

        # check for each available next station whether the connection time would exceed the maximum time of the traject.
        for key in self.connections_dict['connections'].keys():
            if self.time + int(self.connections_dict['connections'][key]) <= self.max_time:
                self.available_connections.append(key)

        # if there are no available connections, this means that the max time will be exceeded if the traject takes a new connection
        # so if this is the case the tim_condition is set to True.
        if len(self.available_connections) == 0:
            self.time_condition = True

    def duration(self):
        """
        This method calculates the total duration of the Traject and stores this in self.time.
        """
        self.time = 0
        for connection in self.connections:
            self.time += int(connection[2])

    def total_connections(self):
        stations_dict, connections_list = read_data(self.stations_path, self.connections_path)
        total_connections = len(connections_list)
        return total_connections

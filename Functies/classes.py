import random
import pprint
from Functies.read_files import read_data

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

    def run(self, stations_path, connections_path):
        """
        This method runs all the functions which are required to make a trajectory.
        """
        self.stations_path = stations_path
        self.connections_path = connections_path
        stations_dict = self.read_csv(stations_path, connections_path)
        # make list of all stations in the data
        stations = []
        for station in stations_dict.keys():
            stations.append(station)

        # choose random station
        start_station = (random.sample(stations, 1)[0])
        self.current_station = start_station
        self.stations.append(start_station)

        # while the max time hasn't been exceeded, available coonnections are determined, a new connection is chosen and added to the list of connections.
        while self.time_condition == False:
            self.determine_available_connections(stations_dict)
            self.add_connection()

            # update the total duration of the traject.
            self.duration()

    def read_csv(self, stations_path, connections_path):
        stations_dict, connections_list = read_data(stations_path, connections_path)
        return stations_dict

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

    def add_connection(self):
        """
        This method randomly chooses a new connection from the available connections and adds this to the list of connections for the traject.
        """
        # check if max time hasn't been exceeded
        if self.time_condition == False:
            # choose random station from available stations
            next_station = random.sample(self.available_connections, 1)[0]

            # a list with the current station, next station and duration of the connection is appended to the connections list.
            self.connections.append([self.current_station, next_station, self.connections_dict['connections'][next_station]])

            # to add the next station to a list of unique stations, it is checked whether the next station is already in the stations list
            if next_station not in self.stations:
                self.stations.append(next_station)

            # set the next station as the current station
            self.current_station = next_station

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

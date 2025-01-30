from Code.Functies.Traject import Traject
import random

class GreedyTraject(Traject):
    def __init__(self):
        super().__init__()

    def run(self, stations_path, connections_path):
        """
        Initialize and run the greedy algorithm for trajectory generation.
        """
        super().run(stations_path, connections_path)

        #Make a list of all stations from the data
        stations = []
        for station in self.stations_dict.keys():
            stations.append(station)

        #Start from a random station
        start_station = random.choice(stations)
        self.current_station = start_station
        self.stations.append(start_station)
        self.previous_station = None

        #While the time limit isn't exceeded
        while self.time_condition == False:
            self.determine_available_connections(self.stations_dict)
            self.add_connection()
            self.duration()

    def determine_available_connections(self, stations_dict):
        """
        Determine the available connections at the current station of the trajectory.
        """
        self.connections_dict = stations_dict[self.current_station]
        self.available_connections = []

        for key, travel_time in self.connections_dict['connections'].items():
            # This checks if connection fits within the time limit and avoid going back unless necessary because
            # there's no other station
            if (self.time + int(travel_time) <= self.max_time and key != self.previous_station):
                self.available_connections.append((key, int(travel_time)))

        # If no new connections are possible, allow returning to the previous station
        if not self.available_connections and self.previous_station:
            travel_time = int(self.connections_dict['connections'][self.previous_station])
            if self.time + travel_time <= self.max_time:
                self.available_connections.append((self.previous_station, travel_time))

        # Sort connections by travel time (with the shortest first) using lambda
        self.available_connections.sort(key=lambda x: x[1])

        # If no connections are available, set the time condition to True
        if not self.available_connections:
            self.time_condition = True

    def add_connection(self):
        """
        Add the shortest connection from the available connections.
        """
        if self.time_condition == False:
            # Choose the shortest connection
            next_station, travel_time = self.available_connections[0]

            # Add the connection to the trajectory
            self.connections.append([self.current_station, next_station, travel_time])

            # Update stations visited in the stations list
            if next_station not in self.stations:
                self.stations.append(next_station)

            # Update previous and current stations
            self.previous_station = self.current_station
            self.current_station = next_station

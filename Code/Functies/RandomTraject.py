from Code.Functies.Traject import Traject
import random

class RandomTraject(Traject):
    def __init__(self):
        super().__init__()

    def run(self, stations_path, connections_path):
        """
        This method chooses a random start station and at every step determines a random next connection to be added to the traject.
        """
        super().run(stations_path, connections_path)
        # make list of all stations in the data
        stations = []
        for station in self.stations_dict.keys():
            stations.append(station)

        # choose random station
        start_station = (random.sample(stations, 1)[0])
        self.current_station = start_station
        self.stations.append(start_station)

        # while the max time hasn't been exceeded, available coonnections are determined, a new connection is chosen and added to the list of connections.
        while self.time_condition == False:
            self.determine_available_connections(self.stations_dict)
            self.add_connection()

            # update the total duration of the traject.
            self.duration()

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

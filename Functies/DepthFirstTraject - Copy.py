from Functies.Traject import Traject
import random
import copy
import pprint

class DepthFirstTraject(Traject):
    def __init__(self):
        self.previous_station = None
        self.states = {}
        self.state_time_condition = False
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

        # initialize the previous station variable (for the first station this doesn't matter since all the available routes will not go to the starting station for the first connection)
        self.previous_station = start_station
        self.stations.append(start_station)

    def depth_first_search(self, depth, stack_max, nr_of_trajects):
        for i in range(nr_of_trajects):
            most_stations = {'stations': [self.current_station], 'duration': 0}
            stack = [[{'stations': [self.current_station], 'duration': 0}]]
            while len(stack) > 0:
                state = stack.pop()
                if len(state[0]['stations']) > len(most_stations['stations']):
                    most_stations = state[0]

                # print(state)
                state_duration = state[0]['duration']
                self.determine_available_connections(self.stations_dict, state[0]['stations'][len(state[0]['stations']) - 1], state_duration)
                if self.state_time_condition == False:
                    if len(state[0]['stations']) < depth:
                        for station in self.available_connections:
                            if len(self.available_connections) > 1 and station != state[0]['stations'][(len(state[0]['stations']) - 2)] or len(self.available_connections) == 1:
                                child = copy.deepcopy(state[0])
                                child['stations'].append(station)
                                child['duration'] += int(self.connections_dict['connections'][station])
                                stack.append([child])
                # print()
                # print("Stack----------------------------------------------------------")
                # print(stack)
                # print("END--------------------------------------------------------------")
                # print()
            pprint.pprint(most_stations)


    def run2(self):
        # while the max time hasn't been exceeded, available coonnections are determined, a new connection is chosen and added to the list of connections.
        while self.time_condition == False:
            self.determine_available_connections(self.stations_dict)
            self.add_connection()

            # update the total duration of the traject.
            self.duration()

    def determine_available_connections(self, stations_dict, station, duration):
        """
        This method determines the available connections at the current station of the traject, and stores these in a self variable as a list.
        """
        # dictionary with the information of the current station
        self.connections_dict = stations_dict[station]
        self.available_connections = []

        # check for each available next station whether the connection time would exceed the maximum time of the traject.
        for key in self.connections_dict['connections'].keys():
            if duration + int(self.connections_dict['connections'][key]) <= self.max_time:
                self.available_connections.append(key)

        # if there are no available connections, this means that the max time will be exceeded if the traject takes a new connection
        # so if this is the case the tim_condition is set to True.
        if len(self.available_connections) == 0:
            self.state_time_condition = True

    def add_connection(self):
        """
        This method randomly chooses a new connection from the available connections and adds this to the list of connections for the traject.
        """
        # check if max time hasn't been exceeded
        if self.state_time_condition == False:
            # choose random station from available stations
            next_station = random.sample(self.available_connections, 1)[0]

            # a list with the current station, next station and duration of the connection is appended to the connections list.
            self.connections.append([self.current_station, next_station, self.connections_dict['connections'][next_station]])

            # to add the next station to a list of unique stations, it is checked whether the next station is already in the stations list
            if next_station not in self.stations:
                self.stations.append(next_station)

            # set the next station as the current station
            self.current_station = next_station

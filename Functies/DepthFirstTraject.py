from Functies.Traject import Traject
import random
import copy
import pprint
from Functies.convert_station_list_to_connections import convert_station_list_to_connections

class DepthFirstTraject(Traject):
    def __init__(self):
        self.previous_station = None
        self.states = {}
        self.state_time_condition = False
        self.trajects = None
        self.all_trajects_connections = []
        self.all_connections = None
        super().__init__()

    def run(self, stations_path, connections_path):
        """
        This method chooses a random start station and at every step determines a random next connection to be added to the traject.
        """
        super().run(stations_path, connections_path)


    def depth_first_search(self, depth, nr_of_trajects):
        """
        This method uses a depth first search to determine the specified number of trajects with the most new connections from a random starting station for each traject.
        """

        total_connections = self.total_connections()

        # make list of all stations in the data
        stations = []
        for station in self.stations_dict.keys():
            stations.append(station)

        # determine starting station for the first traject
        start_station = random.choice(stations)

        # list containing all the connections of all the trajects
        self.all_trajects_connections = []

        # dictionary containing the routes of the individual trajects and their duration
        trajects = {}

        # list with all the visited stations (so that the starting station will always be)
        all_stations = []

        # loop to make a traject for the specified nr of trajects
        for i in range(nr_of_trajects):
            # check if all the connections have not already been done (times 2 because both directions of a connection are added separately to the all_trajects_connections list)
            if len(self.all_trajects_connections) < (total_connections * 2):

                # empty the most_new_connections_list for the new traject
                most_new_connections_list = []

                # set time condition for new traject to False
                self.state_time_condition = False

                # set new_connections to None for new traject
                new_connections = None

                # choose random station that has not already been used
                if len(all_stations) < len(stations):
                    while start_station in all_stations:
                        start_station = random.choice(stations)

                # if all the stations have been used already, a random station is good enough
                else:
                    start_station = random.choice(stations)

                self.current_station = start_station

                # most new connections will contain the traject with the most new connections found using the depth first search
                most_new_connections = {'stations': [self.current_station], 'duration': 0}

                # make stack for the depth first search, starting with just the starting station and duration set to 0
                stack = [[{'stations': [self.current_station], 'duration': 0}]]

                # while loop to loop over the stack
                while len(stack) > 0:
                    self.state_time_condition = False
                    # get the state for the depth first search from the stack
                    state = stack.pop()

                    # make a list of all the connections for the current state
                    state_connections_list = convert_station_list_to_connections(state[0]['stations'])

                    # state new_connections is a list of connections whill contain all the new connections of the current state
                    state_new_connections = []

                    # loop over all the connections in the current state
                    for connection in state_connections_list:

                        # check if they have already been done by this or other trajects, if the connection is new, it is appended to state_new_connections
                        if connection not in self.all_trajects_connections:
                            state_new_connections.append(connection)

                    # if the current state contains more new connections than the previous current traject with the most connections, it is set to be the traject with the most connections
                    if len(state_new_connections) > len(most_new_connections_list):
                        most_new_connections = state[0]

                        # make a most_new_connections_list, so that this one can be compared to future states
                        most_new_connections_list = []
                        most_connections_list = convert_station_list_to_connections(most_new_connections['stations'])
                        for connection in most_connections_list:
                            if connection not in self.all_trajects_connections:
                                most_new_connections_list.append(connection)

                    # set the duration to be the duration of the current state, so that the determine_available_connections function can check if the time limit is exceeded
                    state_duration = state[0]['duration']

                    # determine the available connections
                    self.determine_available_connections(self.stations_dict, state[0]['stations'][len(state[0]['stations']) - 1], state_duration)

                    # if the time condition is still false, a child state can be made
                    if self.state_time_condition == False:

                        # check if the max number of stations hasn't been exceeded TODO: maybe this is unnecessary?
                        if len(state[0]['stations']) < depth:
                            # loop over the stations in the available connections
                            for station in self.available_connections:
                                # make sure that the traject can't go back over the same connection if that isn't the only possibility
                                if len(self.available_connections) > 1 and station != state[0]['stations'][(len(state[0]['stations']) - 2)] or len(self.available_connections) == 1:
                                    # create a child state
                                    child = copy.deepcopy(state[0])

                                    # add the new station and duration to the child state
                                    child['stations'].append(station)
                                    child['duration'] += int(self.connections_dict['connections'][station])

                                    # add the child state to the stack
                                    stack.append([child])

                # set the traject with the most new_connections for the current depth first search as the i'th traject in the traject dictionary
                trajects[i] = most_new_connections

                # make a connection list for the traject with the most new connections in the current depth first search
                connection_list = convert_station_list_to_connections(most_new_connections['stations'])

                # append all the connections that have not been done yet by other trajects to the list with all the trajects
                for connection in connection_list:
                    if connection not in self.all_trajects_connections:
                        self.all_trajects_connections.append(connection)
                        self.all_trajects_connections.append([connection[1], connection[0]])

                # append all new stations to the list with all the stations
                for station in most_new_connections['stations']:
                    if station not in all_stations:
                        all_stations.append(station)

        # store trajects in self so that it can be used later
        self.trajects = trajects


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

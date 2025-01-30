from Code.Functies.Traject import Traject
import random
import copy
import pprint
from Code.Functies.convert_station_list_to_connections import convert_station_list_to_connections

class DepthFirstTraject(Traject):
    def __init__(self):
        self.previous_station = None
        self.states = {}
        self.state_time_condition = False
        self.trajects = {}
        self.all_trajects_connections = []
        self.all_connections = None
        self.traject_durations = {}
        super().__init__()

    def depth_first_search(self, depth, nr_of_trajects, stations_path, connections_path):
        """
        This method uses a depth first search to determine the specified number of trajects with the most new connections from a random starting station for each traject.
        """
        self.run(stations_path, connections_path)
        total_connections = self.total_connections()

        # make list of all stations in the data
        stations = []
        for station in self.stations_dict.keys():
            stations.append(station)

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

                # empty the best_solution_total_connections_list for the new traject
                best_solution_total_connections = []

                # set time condition for new traject to False
                self.state_time_condition = False

                # set new_connections to None for new traject
                new_connections = None

                # determine the starting station for the current traject
                self.station_choice(all_stations, stations)

                # most new connections will contain the traject with the most new connections found using the depth first search
                best_solution_stations = {'stations': [self.current_station], 'duration': 0}

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
                    if len(state_new_connections) > len(best_solution_total_connections):
                        best_solution_total_connections, best_solution_stations = self.save_solution(state, state_new_connections, best_solution_total_connections)
                        self.traject_durations[i] = state[0]['duration']

                    # set the duration to be the duration of the current state, so that the determine_available_connections function can check if the time limit is exceeded
                    state_duration = state[0]['duration']

                    # determine the available connections
                    self.determine_available_connections(self.stations_dict, state[0]['stations'][len(state[0]['stations']) - 1], state_duration)

                    # run build children function to add all possible children to the stack
                    stack = self.build_children(depth, state, stack, station)

                # set the traject with the most new_connections for the current depth first search as the i'th traject in the traject dictionary
                trajects[i] = best_solution_stations


                # make a connection list for the traject with the most new connections in the current depth first search
                connection_list = convert_station_list_to_connections(best_solution_stations['stations'])

                # append all the connections that have not been done yet by other trajects to the list with all the trajects
                for connection in connection_list:
                    if connection not in self.all_trajects_connections:
                        self.all_trajects_connections.append(connection)
                        self.all_trajects_connections.append([connection[1], connection[0]])

                # append all new stations to the list with all the stations
                for station in best_solution_stations['stations']:
                    if station not in all_stations:
                        all_stations.append(station)

        # store trajects in self so that it can be used later
        self.generate_output(trajects)
        self.connections = self.all_trajects_connections


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

    def build_children(self, depth, state, stack, station):
        """
        This method adds the possible children to the depth first search stack.
        """
        # if the time condition is still false, a child state can be made
        if self.state_time_condition == False:

            # check if the max number of stations hasn't been exceeded
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
        return stack

    def save_solution(self, state, state_new_connections, best_solution_total_connections):
        """
        This method checks if the current state is better than the previously stored best state, and
        if that is the case it saves the state.
        """

        best_solution_stations = state[0]

        # make a best_solution_total_connections list, so that this solution one can be compared to future states
        best_solution_total_connections = []
        most_connections_list = convert_station_list_to_connections(best_solution_stations['stations'])
        for connection in most_connections_list:
            if connection not in self.all_trajects_connections:
                best_solution_total_connections.append(connection)
        return best_solution_total_connections, best_solution_stations

    def station_choice(self, all_stations, stations):
        """
        This method chooses a random starting station for the trajects of the depth first search,
        from the pool of stations where not all connections have been done yet.
        """

        count = 0
        connections = []

        # determine starting station for the traject, the loop makes sure that at least 1 connection of the starting station has not been done yet.
        while count == len(connections):
            start_station = random.choice(stations)

            connections = []
            for key in self.stations_dict[start_station]['connections'].keys():
                connections.append([start_station, key])

            count = 0
            for connection in connections:
                if connection in self.all_trajects_connections:
                    count += 1

        # store the current station in the object
        self.current_station = start_station

    def generate_output(self, trajects):
        # make the connections_list for the visualization

        traject_list = []

        for key in trajects.keys():
            station_list= []
            station_list = trajects[key]['stations']
            connection_list = convert_station_list_to_connections(station_list)
            for i in range(len(connection_list)):
                connection_list[i].append(0)

            traject_list.append(connection_list)
        count = 0

        for traject in traject_list:
            count += 1

            self.trajects[count] = traject

    def state_duration(self, state):
        """
        This method calculates the duration of a state.
        """
        state_stations = state[0]['stations']
        time = 0

        # loop over all the stations in a state to add all the durations of the connections
        for i in range(len(state_stations)):
            # the last station in the list does not have a connection so that is why this check is done.
            if i < len(state_stations) - 1:
                station1 = state_stations[i]
                station2 = state_stations[i + 1]
                time += int(self.stations_dict[station1]['connections'][station2])
        return time

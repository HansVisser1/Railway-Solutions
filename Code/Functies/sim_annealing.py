from Code.Functies.RandomTraject import RandomTraject
from Code.Functies.calculate_score import calculate_score
import random
import copy
import math

def sim_annealing(nr_of_trajects, iterations, stations_path, connections_path, time_limit, temp=120, cooling_rate=0.9999):
    """
    This function randomly adds a connection to an end of the trajects, and if this improves the quality,
    the new state is saved. Also there is a temperature, which will introduce a probability to accept
    a new state that is worse than the previous state.
    """
    # list to determine which side of traject to edit
    back_or_front = [0, -1]
    state = []

    # temperature
    T = temp

    # add trajects to state using random algorithm
    for i in range(nr_of_trajects):
        traject = RandomTraject()
        traject.max_time = time_limit
        traject.run(stations_path, connections_path)
        state.append(traject)

    # this list contains the state connections per traject
    all_trajects_state = []
    unique_connections = []
    total_time = 0
    for traject in state:
        # add the connections to the list
        all_trajects_state.append(traject.connections)

        # loop over the connections themselves to add them to the unique connections list and calculate the total time of the traject.
        for connection in traject.connections:
            total_time += int(connection[2])
            if connection not in unique_connections:
                unique_connections.append(connection)
                unique_connections.append([connection[1], connection[0], connection[2]])

    total_connections = traject.total_connections()
    # calculate the quality of the randomly made state.
    quality = calculate_score(len(unique_connections) / 2, nr_of_trajects, total_connections, total_time)

    for iter in range(iterations):
        # the count is used so that the different trajects within the state are edited one after the other
        count = 0

        # count can't be higher than the amount of trajects in the state
        if count > len(state):
            count = 0

        # duration of the current traject
        state[count].duration()
        traject_duration = state[count].time

        # choose if the back or front of the traject will be expanded
        back_or_front_choice = random.choice(back_or_front)

        # get the connection at the end that will be expanded
        traject_end_connection = state[count].connections[back_or_front_choice]

        # this condition is used to later append and pop the correct connections from the traject.
        front_condition = None

        # determine the end station
        if back_or_front_choice == 0:
            end_station = traject_end_connection[0]
            front_condition = True
        else:
            end_station = traject_end_connection[1]
            front_condition = False

        # determine the possible connections
        possible_connections = []
        for key in traject.stations_dict[end_station]['connections'].keys():
            possible_connections.append([end_station, key, traject.stations_dict[end_station]['connections'][key]])

        # make list for the possible child trajects
        children = []

        # make the child trajects and put them in the list
        for i in range(len(possible_connections)):
            # I don't want to edit the state directly so I need to make a copy
            connections = copy.deepcopy(state[count].connections)

            # insert the new connection
            if front_condition == True:
                connections.insert(0, possible_connections[i])
            else:
                connections.append(possible_connections[i])

            # remove connection if the duration is too long
            if traject_duration + int(possible_connections[i][2]) > traject.max_time:
                if front_condition == True:
                    connections.pop(-1)
                else:
                    connections.pop(0)
            children.append(connections)

        # choose random child
        child = random.choice(children)
        unique_connections = []
        original_state = copy.deepcopy(state[count].connections)

        # set the child traject as the new traject
        state[count].connections = child
        all_trajects_state = []
        total_time = 0

        # loop to get all_trajects_state, unique connections and the total time
        for traject in state:
          all_trajects_state.append(traject.connections)
          for connection in traject.connections:
           total_time += int(connection[2])
           if connection not in unique_connections:
               unique_connections.append(connection)
               unique_connections.append([connection[1], connection[0], connection[2]])

        # quality of the new state
        new_quality = calculate_score(len(unique_connections) / 2, len(all_trajects_state), total_connections, total_time)
        delta_quality = new_quality - quality

        # if the new quality is better set it as the quality
        if new_quality >= quality:
             quality = new_quality

        # if the quality is worse, apply chance to get it accepted.
        else:
            acceptance_probability = math.exp(delta_quality / T)
            if random.random() < acceptance_probability:
                quality = new_quality

            # if the state doesn't get accepted revert to old state.
            else:
                state[count].connections = original_state

        # make the all_trajects_state for the output
        all_trajects_state = []
        for traject in state:
          all_trajects_state.append(traject.connections)

         # add to count so that in the next loop the next traject is edited
        count += 1

        # cool the temperature down
        if T > 0.000000001:
            T *= cooling_rate

    return all_trajects_state, quality

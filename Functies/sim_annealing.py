from Functies.RandomTraject import RandomTraject
from Functies.calculate_score import calculate_score
import random
import copy
import math

def sim_annealing(nr_of_trajects, iterations, stations_path, connections_path):
    back_or_front = [0, -1]
    starting_state = []
    T = 100


    for i in range(nr_of_trajects):
        traject = RandomTraject()
        traject.run(stations_path, connections_path)
        starting_state.append(traject)

    all_trajects_state = []
    unique_connections = []
    for state in starting_state:
        all_trajects_state.append(state.connections)
        total_time = 0
        for connection in state.connections:
            total_time += int(connection[2])
            if connection not in unique_connections:
                unique_connections.append(connection)
                unique_connections.append([connection[1], connection[0], connection[2]])

    quality = calculate_score(len(unique_connections) / 2, len(all_trajects_state), traject.total_connections(), total_time)

    for iter in range(iterations):
        # if iter % 100 == 0:
        #     print(f"iteration {iter}/{iterations}")


        count = 0
        if count > len(starting_state):
            count = 0

        starting_state[count].duration()
        traject_duration = starting_state[count].time

        back_or_front_choice = random.choice(back_or_front)
        traject_end_connection = starting_state[count].connections[back_or_front_choice]

        front_condition = None
        if back_or_front_choice == 0:
            end_station = traject_end_connection[0]
            front_condition = True
        else:
            end_station = traject_end_connection[1]
            front_condition = False


        possible_connections = []
        for key in traject.stations_dict[end_station]['connections'].keys():
            possible_connections.append([end_station, key, traject.stations_dict[end_station]['connections'][key]])

        children = []
        new_state = None

        for i in range(len(possible_connections)):

            connections = copy.deepcopy(starting_state[count].connections)

            if front_condition == True:
                connections.insert(0, possible_connections[i])
            else:
                connections.append(possible_connections[i])

            if traject_duration + int(possible_connections[i][2]) > traject.max_time:
                if front_condition == True:
                    connections.pop(-1)
                else:
                    connections.pop(0)

            children.append(connections)

        child = random.choice(children)
        unique_connections = []

        original_state = copy.deepcopy(starting_state[count].connections)
        starting_state[count].connections = child
        all_trajects_state = []
        for state in starting_state:
          all_trajects_state.append(state.connections)
          total_time = 0
          for connection in state.connections:
           total_time += int(connection[2])
           if connection not in unique_connections:
               unique_connections.append(connection)
               unique_connections.append([connection[1], connection[0], connection[2]])

        new_quality = calculate_score(len(unique_connections) / 2, len(all_trajects_state), traject.total_connections(), total_time)

        delta_quality = new_quality - quality
        if new_quality >= quality:
             if new_quality > quality:
                 pass
                 # print(f"quality improved {new_quality - quality}")
             quality = new_quality
        else:
            acceptance_probability = math.exp(delta_quality / T)
            if random.random() < acceptance_probability:
                # print(f"quality decreased {new_quality - quality}")
                quality = new_quality
            else:
                starting_state[count].connections = original_state



        all_trajects_state = []
        for state in starting_state:
            all_trajects_state.append(state.connections)
        count += 1

        if T > 0.000000001:
            T *= 0.99


    return all_trajects_state, quality

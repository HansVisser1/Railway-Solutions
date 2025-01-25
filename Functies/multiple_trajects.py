from Functies.Traject import Traject
from Functies.RandomTraject import RandomTraject
from Functies.greedy import GreedyTraject
from Functies.hillclimber import hillclimber
from Functies.sim_annealing import sim_annealing

from Functies.calculate_score import calculate_score
from Functies.DepthFirstTraject import DepthFirstTraject


def multiple_trajects(nr, traject_type, stations_path, connections_path, DFS_depth, algorithm_iterations):
    """
    this function multiple trajects and puts them in a list
    """
    trajects = []
    total_connections_trajects = []
    total_time = 0
    if traject_type == 'DepthFirst':
        traject = DepthFirstTraject()
        traject.depth_first_search(DFS_depth, nr, stations_path, connections_path)
        trajects = traject.trajects
        connection_nr = len(traject.all_trajects_connections) / 2
        new_nr = len(trajects.keys())
        for key in traject.traject_durations.keys():
            total_time += traject.traject_durations[key]
        total_connections = traject.total_connections()
        quality = calculate_score(connection_nr, nr, total_connections, total_time)
    else:
        new_nr = nr
        trajects = []
        if traject_type == 'HillClimber':
            trajects, quality = hillclimber(nr, algorithm_iterations, stations_path, connections_path)
        if traject_type == 'SimulatedAnnealing':
            trajects, quality = sim_annealing(nr, algorithm_iterations, stations_path, connections_path)
        elif traject_type == 'Random' or traject_type == 'Greedy':
            for i in range(nr):
                if traject_type == 'Random':
                    traject = RandomTraject()
                if traject_type == 'Greedy':
                    traject = GreedyTraject()
                traject.run(stations_path, connections_path)
                trajects.append(traject)
                total_time += traject.time

                for connection in traject.connections:
                    if connection not in total_connections_trajects:
                        total_connections_trajects.append(connection)
                        total_connections_trajects.append([connection[1], connection[0], connection[2]])

            connection_nr = len(total_connections_trajects) / 2
            total_connections = trajects[0].total_connections()

            if connection_nr > total_connections:
                print(connection_nr)
                print(total_connections)
                print(total_connections_trajects)
                print("Error in connections_nr")

            quality = calculate_score(connection_nr, nr, total_connections, total_time)
    return trajects, quality, new_nr

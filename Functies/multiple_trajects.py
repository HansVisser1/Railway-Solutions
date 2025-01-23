from Functies.Traject import Traject, RandomTraject
from Functies.greedy import GreedyTraject

from Functies.calculate_score import calculate_score
from Functies.DepthFirstTraject import DepthFirstTraject


def multiple_trajects(nr, traject_type, stations_path, connections_path, DFS_depth):
    """
    this function multiple trajects and puts them in a list
    """
    trajects = []
    total_connections_trajects = []
    total_time = 0
    if traject_type == 'DepthFirst':
        traject = DepthFirstTraject()
        traject.run(stations_path, connections_path)
        traject.depth_first_search(DFS_depth, nr)
        trajects = traject.trajects
        connection_nr = len(traject.all_trajects_connections) / 2
        new_nr = len(trajects.keys())

        total_connections = traject.total_connections()
    else:
        new_nr = nr
        trajects = []
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

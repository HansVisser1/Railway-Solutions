from Functies.Traject import Traject
from Functies.RandomTraject import RandomTraject
from Functies.greedy import GreedyTraject
from Functies.hillclimber import hillclimber
from Functies.sim_annealing import sim_annealing

from Functies.calculate_score import calculate_score
from Functies.DepthFirstTraject import DepthFirstTraject


def multiple_trajects(nr, traject_type, stations_path, connections_path, DFS_depth, algorithm_iterations, time_limit):
    """
    this function makes the specified output with multiple trajects. since the output of the different algorithms varies, the process is different
    for the different algorithms.
    """

    # some of the algorithms use this list
    trajects = []
    total_connections_trajects = []
    total_time = 0


    if traject_type == 'DepthFirst':
        # make object
        traject = DepthFirstTraject()
        traject.max_time = time_limit
        traject.depth_first_search(DFS_depth, nr, stations_path, connections_path)

        # set trajects to the found solution
        trajects = traject.trajects

        # count the number of travelled connections
        connection_nr = len(traject.all_trajects_connections) / 2

        # determine how many trajects have been done (with depth first this might not be equal to the specified number, since depthfirst stops as soon as all connections have been done)
        new_nr = len(trajects.keys())

        # determine the total time of the solution
        for key in traject.traject_durations.keys():
            total_time += traject.traject_durations[key]

        # determine the total amount of connections
        total_connections = traject.total_connections()

        # calculate the quality of the solution
        quality = calculate_score(connection_nr, nr, total_connections, total_time)
    else:
        # since this function outputs the new_nr to make sure the correct nr of trajectories stored, the new_nr is set to the input nr here.
        # because the only algorithm where the new nr can be different is with depth first.
        new_nr = nr
        trajects = []

        # generate output for hillclimber & simulated annealing algorithms
        if traject_type == 'HillClimber':
            trajects, quality = hillclimber(nr, algorithm_iterations, stations_path, connections_path, time_limit)
        elif traject_type == 'SimulatedAnnealing':
            trajects, quality = sim_annealing(nr, algorithm_iterations, stations_path, connections_path, time_limit)

        # make output for random or greedy algorithms
        elif traject_type == 'Random' or traject_type == 'Greedy':

            # loop to make the specified nr of trajects
            for i in range(nr):
                # make objects
                if traject_type == 'Random':
                    traject = RandomTraject()
                elif traject_type == 'Greedy':
                    traject = GreedyTraject()

                # run objects
                traject.max_time = time_limit
                traject.run(stations_path, connections_path)
                trajects.append(traject)
                total_time += traject.time

                # list the total connections of the trajects to determine the amount of unique connections
                for connection in traject.connections:
                    if connection not in total_connections_trajects:
                        total_connections_trajects.append(connection)
                        total_connections_trajects.append([connection[1], connection[0], connection[2]])

            # determine unique connections and total connections for random and greedy
            connection_nr = len(total_connections_trajects) / 2
            total_connections = trajects[0].total_connections()

            # calculate quality for random and greedy
            quality = calculate_score(connection_nr, nr, total_connections, total_time)
    return trajects, quality, new_nr

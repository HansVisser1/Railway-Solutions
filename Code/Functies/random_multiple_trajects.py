import random
from Code.Functies.multiple_trajects import multiple_trajects

def random_multiple_trajects(traject_type, min, max, stations_path, connections_path, DFS_depth, algorithm_iterations, time_limit):
    """
    This function generates a random number in the given range and generates that amount of trajects.
    """
    nr = random.randint(min, max)
    trajects, cost, new_nr = multiple_trajects(nr, traject_type, stations_path, connections_path, DFS_depth, algorithm_iterations, time_limit)
    return new_nr, trajects, cost

import random
from Functies.multiple_trajects import multiple_trajects

def random_multiple_trajects(min, max, stations_path, connections_path):
    """
    This function generates a random number in the given range and generates that amount of trajects.
    """
    nr = random.randint(min, max)
    trajects, cost = multiple_trajects(nr, stations_path, connections_path)
    return nr, trajects, cost

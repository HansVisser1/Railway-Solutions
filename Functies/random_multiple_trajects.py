import random
from Functies.multiple_trajects import multiple_trajects

def random_multiple_trajects(min, max):
    """
    This function generates a random number in the given range and generates that amount of trajects.
    """
    nr = random.randint(min, max + 1)
    trajects, cost = multiple_trajects(nr)
    return trajects, cost

import csv

def highest_score_convert(best_trajects, traject_type):
    """
    This method returns the best trajects of the baseline in a format that is compatible with the visualisation.  This format is as follows: [List of Trajects] where
    each list of a traject is as follows: [list of connections], where each list of connections is as follows: [station1, station2, duration].
    """
    # converts the best_trajects according to what it is with random and greedy
    if traject_type == 'Random' or traject_type == 'Greedy':
        traject_connections = []
        for traject in best_trajects:
            traject_connections.append(traject.connections)
        return traject_connections

    # converts the best_trajects according to what it is with hillclimber and simulated annealing
    elif traject_type == 'HillClimber' or traject_type == 'SimulatedAnnealing':
        return best_trajects

    # converts the best_trajects according to what it is with depth first
    elif traject_type == 'DepthFirst':
        traject_connections = []
        for key in best_trajects.keys():
            traject_connections.append(best_trajects[key])
        return traject_connections

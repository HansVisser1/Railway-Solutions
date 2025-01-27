import csv

def highest_score_convert(best_trajects, traject_type):
    """
    This method returns the best trajects of the baseline in a format that is compatible with the visualisation,
    and it saves the best traject in a csv file in the same format. This format is as follows: [List of Trajects] where
    each list of a traject is as follows: [list of connections], where each list of connections is as follows: [station1, station2, duration].
    """
    with open(f"highest_score_csv_{traject_type}.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow([traject_type])
        if traject_type == 'Random' or traject_type == 'Greedy':
            traject_connections = []
            for traject in best_trajects:
                traject_connections.append(traject.connections)
            return traject_connections
        elif traject_type == 'HillClimber' or traject_type == 'SimulatedAnnealing':
            return best_trajects
        elif traject_type == 'DepthFirst':
            traject_connections = []
            for key in best_trajects.keys():
                traject_connections.append(best_trajects[key])
            return traject_connections

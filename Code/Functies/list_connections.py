from Code.Functies.Traject import Traject

def list_connections(traject_list):
    """
    This function takes the connections for each trajects and appends them to a list, which is then returned.
    """
    connections_list = []
    for traject in traject_list:
        connections_list.append(traject.connections)
    return connections_list

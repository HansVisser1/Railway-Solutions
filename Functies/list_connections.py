from Functies.classes import Traject

def list_connections(traject_list):
    connections_list = []
    for traject in traject_list:
        connections_list.append(traject.connections)
    return connections_list

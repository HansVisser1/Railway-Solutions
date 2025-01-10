from Functies.classes import Traject
from Functies.calculate_score import calculate_score


def multiple_trajects(nr):
    """
    this function multiple trajects and puts them in a list
    """
    trajects = []
    stations = []
    total_time = 0
    for i in range(nr):
        traject = Traject()
        traject.run('Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv')
        trajects.append(traject)
        total_time += traject.time
        for station in traject.stations:
            if station not in stations:
                stations.append(station)
    station_nr = len(stations)
    total_connections = trajects[0].total_connections()
    cost = calculate_score(station_nr, nr, total_connections, total_time)
    return trajects, cost

def calculate_score(station_nr, traject_nr, total_connections, total_time):
    """
    This function calculates the score K = p*10000 - (T*100 + Min)
    """
    p = (station_nr) - 1 / total_connections
    T = traject_nr
    Min = total_time
    return int(p * 10000 - (T * 100 + Min))

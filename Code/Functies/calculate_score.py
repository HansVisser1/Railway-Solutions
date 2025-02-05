def calculate_score(connection_nr, traject_nr, total_connections, total_time):
    """
    This function calculates the score K = p*10000 - (T*100 + Min)
    """
    p = connection_nr / total_connections
    T = traject_nr
    Min = total_time
    return float(p * 10000 - (T * 100 + Min))

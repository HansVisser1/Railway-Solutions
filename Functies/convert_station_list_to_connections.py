def convert_station_list_to_connections(station_list):
    """
    This method takes a station list of a traject (in order of when the train passes the station), and converts it to a connection list in the format that it is used by the other parts of this algorithm.
    """
    connection_list = []
    for i in range(len(station_list) - 1):
        connection_list.append([station_list[i], station_list[i+1]])
    return connection_list

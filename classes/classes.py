
class Station():
    def __init__(self, name, x_coord, y_coord):
        """
        This method stores the name and coordinates of the station in the station object.
        """
        self.name = name
        self.x = x_coord
        self.y = y_coord

class Connection():
    def __init__(self, time, station1, station2):
        """
        This method stores the duration and the connected stations in the connection object.
        """
        self.time = time
        self.stations = [station1.name, station2.name]

class Traject():
    def __init__(self):
        """
        The init method initializes a route list, which is kept empty, a time value which is set to None and
        the method stores the connections_list in the Traject object.
        """
        self.stations = []
        self.connections = []
        self.time = None
        self.max_time = 120
        self.time_condition = False

    def add_connection(self, connection):
        """
        This method adds a connection to the connections list stored in the Traject object
        """
        self.connections.append(connection)

    def add_connections(self, connections_list):
        """
        This methods adds connections from a list to the Traject object as long as they don't exceed the maximum time.
        It also checks whether the station can be connected.
        """

        for connection in connections_list:
            if len(self.connections) == 0:
                add_connection(connection)
            # else:
            #     if connection.stations[0] in self.stations or connection.stations[1] in self.stations:
            #         if duration() + connection.time <= 120:
            #             add_connection(connection)


    def stations(self):
        for connection in self.connections:
            if connection.stations[0] not in self.stations:
                self.stations.append(connection.stations[0])
            if connection.stations[1] not in self.stations:
                self.stations.append(connection.stations[1])

    def duration(self):
        """
        This method calculates the duration of the Traject
        """
        self.time = 0
        for connection in self.connections:
            self.time += connection.time
        return self.time

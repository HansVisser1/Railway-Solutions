import pprint
from Functies.classes import Traject
from Functies.read_files import read_data
from Functies.random_multiple_trajects import random_multiple_trajects
from Functies.baseline import baseline
from Functies.list_connections import list_connections
import Visualisation.visualize_railway

nr, trajects, cost = random_multiple_trajects(1, 7)
connections_list = list_connections(trajects))

#print(baseline(100))

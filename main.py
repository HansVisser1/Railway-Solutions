import pprint
from Functies.classes import Traject
from Functies.read_files import read_data
from Functies.random_multiple_trajects import random_multiple_trajects
import Visualisation.visualize_railway

nr, trajects, cost = random_multiple_trajects(1, 7)
print(f"cost: {cost}")
for traject in trajects:
    print(traject.connections)
    print()

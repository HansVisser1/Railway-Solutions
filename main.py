import pprint
from Functies.classes import Traject
from Functies.read_files import read_data
import Visualisation.visualize_railway

traject1 = Traject()
traject1.run('Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv')
print(traject1.connections)
print(traject1.time)

score = traject1.calculate_score()
print(f"Trajectory Score: {score}")

stations, connections = read_data('Data/StationsHolland.csv', 'Data/ConnectiesHolland.csv')
# pprint.pprint(stations)
# pprint.pprint(connections)

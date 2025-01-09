from classes import Traject


traject1 = Traject()
traject1.run('StationsHolland.csv', 'ConnectiesHolland.csv')
print(traject1.connections)
print(traject1.time)

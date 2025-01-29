# RailNL
Railway Solutions
The goal of this case is making a route planning for a train network for Holland and for the Netherlands.
For Holland there can be a max of 7 routes and for the Netherlands there can be a max of 20 routes in the network.
The routes should fit in the specified time limit (120 minutes for Holland and 180 minutes for the Netherlands).
For a good solution the routes should travel over as much connections as possible within the time limit, 
while avoiding overlapping too much with other routes.

**Requirements**

All the code is in Python. The requirements.txt contains all the necessary packages to run the code successfully. 
by running this in the terminal the packages can be installed:
'pip install -r requirements.txt'

**USAGE**

The planning can be made by running 'python main.py' from the main folder.
Within the main.py file parameters can be changed to run the different algorithms for the different networks.
These parameters are explained within the main.py file.

**RUNNING sim_annealing_experiment.py:**

Temp & Cooling rate simulated annealing:
Scroll down in 'sim_annealing_experiment.py'. At the bottom of the file the parameters for the experiment can be set.
Then run file through the terminal with 'python sim_annealing_experiment.py'

**RUNNING experiment.py**

This runs all 5 algorithms and plots them in a graph. On the x-axis the time it takes and on the y-axis the max quality score the algorithm has untill that point.
From line 15 to 21 are the parameters to run the file. Default is set for the entire Netherlands with max 20 trajectories.
Max time is the time in seconds the algorithms are allowed to run. Its either capped by the time or the amount of iterations, which is by default set to very high.
Run the file through the terminal with 'python experiment.py'

**Structure**

This is a list describing the data structure of this project and what the different folders contain:

/Code: This folder contains all the code of the project.

Code/Functies: This folder contains all the functions that were made

Code/Visualisation: This folder contains all the code with regards to visualising the outputs of the algorithms

/Data: This folder contains information about the stations and connections in the networks for Holland and the Netherlands that the code uses to make the routes, as well as the geojson files to visualize the maps.

/Results: This folder contains all the plots and outputs of the code.

Results/Plotted_figures: This folder contains all the figures that will be plotted by the code.

**Authors**

Hans Visser
Victor Brouns
Leander Gall

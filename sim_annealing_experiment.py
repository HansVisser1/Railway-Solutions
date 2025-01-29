from Functies.sim_annealing import sim_annealing
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import numpy as np
import time

time_limit = 120

stations = 'Data/StationsHolland.csv'
connections = 'Data/ConnectiesHolland.csv'
stations_nl = 'Data/StationsNationaal.csv'
connections_nl = 'Data/ConnectiesNationaal.csv'

def sim_annealing_temperature_test(iterations, min_temp, max_temp, step_size, min_cooling, max_cooling, cooling_step_size, algorithm_iterations, stations_path, connections_path, min_trajects, max_trajects, time_limit):
    """
    This function runs simulated annealing for all the combinations within the temperature and cooling rate range. It saves it to a csv.
    """
    # create list containing all the temperatures that will be done
    temps = []
    temperature= min_temp
    if temperature == 0:
        temperature = 0.000000001
    while temperature <= max_temp:
        temps.append(temperature)
        temperature += step_size

    # create list containing all the cooling rates that will be done
    cooling_rates = []
    cooling_rate = min_cooling
    while cooling_rate <= max_cooling:
        cooling_rates.append(cooling_rate)
        cooling_rate += cooling_step_size   
    
    # make csv writer with the correct collumns
    with open('simulated_annealing_temp_test.csv', 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['nr of trajects', 'temperature', 'cooling rate', 'quality'])

        count = 0
        start = time.perf_counter()

        # running the specified amount of iterations for every temperature and cooling rate
        for temp in temps:
            print(f"step {count}/{len(temps)*len(cooling_rates)}")
            for cooling_rate in cooling_rates:
                for i in range(iterations):
                    # make the state and calculate the quality
                    nr_of_trajects = random.randint(min_trajects, max_trajects)
                    state, quality = sim_annealing(nr_of_trajects, algorithm_iterations, stations_path, connections_path, time_limit, temp, cooling_rate)
                    writer.writerow([nr_of_trajects, temp, cooling_rate,  quality])
                    end = time.perf_counter()

                    # print statement to keep track of running time
                    if i % 25 == 0:
                        print(f"step {count}/{len(temps)*len(cooling_rates)}: {(i/iterations)*100}%")
                        if (end - start) < 60:
                            print(f"The experiment has been running for {int(end - start)} seconds")
                        elif 120 > (end - start) > 60:
                            print(f"The experiment has been running for {int((end - start) / 60)} minute and {int((end - start) % 60)} seconds")
                        else:
                            print(f"The experiment has been running for {int((end - start) / 60)} minutes and {int((end - start) % 60)} seconds")
                
                count += 1



def plot_sim_annealing_temp_test(file='simulated_annealing_temp_test_nl.csv'):
    """
    This function takes the csv file and plots the results in a heatmap plot
    """
    # make dataframe
    df = pd.read_csv(file)
    df['temperature'] = df['temperature'].astype(int)

    # pivot the dataframe so that it can be turned into a heatmap
    heatmap_data = df.pivot_table(
    index='cooling rate',  # rows
    columns='temperature',  # columns
    values='quality',  # cells
    aggfunc='mean'  # calculate the mean for the qualities for each combination of cooling rate and temperature
)
    # make the plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        data=heatmap_data,
        cmap='coolwarm',  # Use a diverging colormap
        annot=False,  # Set to True to display values in the cells
        cbar_kws={'label': 'Quality'},  # Label for the color bar
    )
    plt.yticks(rotation=0)
    plt.title('Quality by Temperature and Cooling Rate. Simulated Annealing (50 iterations)')
    plt.xlabel('Temperature')
    plt.ylabel('Cooling Rate')

    # saving figure as png image
    plt.savefig('Simulated_Annealing_experiment_nl.png', bbox_inches = 'tight')
    plt.show()


# arguments for sim_annealing_temperature_test function:
# (iterations, min_temp, max_temp, step_size, min_cooling, max_cooling, cooling_step_size, algorithm_iterations, stations_path, connections_path, min_trajects, max_trajects)
# sim_annealing_temperature_test(500, 0, 650, 50, 0.980, 0.999, 0.001, 2000, stations, connections, 1, 7)
sim_annealing_temperature_test(50, 0, 650, 50, 0.9980, 0.9999, 0.0001, 10000, stations_nl, connections_nl, 1, 20, 180)
plot_sim_annealing_temp_test()

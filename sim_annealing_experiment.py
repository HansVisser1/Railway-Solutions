from sim_annealing import sim_annealing
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import numpy as np

stations = 'Data/StationsHolland.csv'
connections = 'Data/ConnectiesHolland.csv'
def sim_annealing_temperature_test(iterations, min_temp, max_temp, step_size, min_cooling, max_cooling, cooling_step_size, algorithm_iterations, stations_path, connections_path, min_trajects, max_trajects):

    temps = []
    temperature= min_temp
    if temperature == 0:
        temperature = 0.000000001

    cooling_rates = []
    cooling_rate = min_cooling
    while cooling_rate <= max_cooling:
        cooling_rates.append(cooling_rate)
        cooling_rate += cooling_step_size


    while temperature <= max_temp:
        temps.append(temperature)
        temperature += step_size

    with open('simulated_annealing_temp_test.csv', 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['nr of trajects', 'temperature', 'cooling rate', 'quality'])


        count = 0
        for temp in temps:
            print(f"step {count}/{len(temps)*len(cooling_rates)}")
            for cooling_rate in cooling_rates:
                for i in range(iterations):
                    print(f"step {count}/{len(temps)*len(cooling_rates)}: {(i/iterations)*100}%")
                    nr_of_trajects = random.randint(min_trajects, max_trajects)
                    state, quality = sim_annealing(nr_of_trajects, algorithm_iterations, stations_path, connections_path, temp)
                    writer.writerow([nr_of_trajects, temp, cooling_rate,  quality])

                count += 1


def plot_sim_annealing_temp_test(file='simulated_annealing_temp_test.csv'):
    df = pd.read_csv(file)
    # normalized_df=(df-df.min())/(df.max()-df.min())
    # normalized_df['temp_cooling_rate'] = normalized_df.apply(lambda row: f"{row['temperature']}-{row['cooling rate']}", axis=1)
    # print(normalized_df)
    df['temperature'] = df['temperature'].astype(int)
    heatmap_data = df.pivot_table(
    index='cooling rate',  # Rows
    columns='temperature',  # Columns
    values='quality',  # Cell values
    aggfunc='mean'  # Aggregate multiple entries
)
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        data=heatmap_data,
        cmap='coolwarm',  # Use a diverging colormap
        annot=False,  # Set to True to display values in the cells
        cbar_kws={'label': 'Quality'},  # Label for the color bar
    )
    plt.title('Heatmap of Quality by Temperature and Cooling Rate')
    plt.xlabel('Temperature')
    plt.ylabel('Cooling Rate')
    plt.show()

     # saving figure as png image
    plt.savefig('Simulated_Annealing_experiment.png', bbox_inches = 'tight')
    plt.show()


# arguments for sim_annealing_temperature_test function:
# (iterations, min_temp, max_temp, step_size, min_cooling, max_cooling, cooling_step_size, algorithm_iterations, stations_path, connections_path, min_trajects, max_trajects)
sim_annealing_temperature_test(50, 0, 500, 50, 0.985, 0.999, 0.001, 2000, stations, connections, 1, 7)
plot_sim_annealing_temp_test()

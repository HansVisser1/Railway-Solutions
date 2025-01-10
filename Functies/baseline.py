from Functies.random_multiple_trajects import random_multiple_trajects
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

def baseline(iterations):
    cost_dict = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
    for i in range(iterations):
        nr, trajects, cost = random_multiple_trajects(1, 7)
        cost_dict[nr].append(cost)

    for key in cost_dict.keys():
        sum = 0
        average = None
        for value in cost_dict[key]:
            sum += value
        average = sum / len(cost_dict[key])
        cost_dict[key] = average


    cost_series = pd.Series(cost_dict)
    df = pd.DataFrame()
    df['Cost'] = cost_series
    sns.relplot(df, x = df.index, y = "Cost", kind="line")
    plt.xlabel("Number of trains")
    plt.ylabel("Cost")
    plt.show()
    return cost_dict

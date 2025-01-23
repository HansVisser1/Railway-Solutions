from Functies.list_connections import list_connections
import pprint
def traject_list(trajects, traject_type):
    """
    This function prints the output and creates the list of connections which is required for the visualization.
    """
    if traject_type == 'DepthFirst':
        traject_list = []

        # loop over the trajects dictionary of the depthfirst object
        for key in trajects.keys():
            traject_list.append(trajects[key])
    else:
        traject_list = list_connections(trajects)

    # print the output
    count = 0
    for traject in traject_list:
        count += 1
        pprint.pprint(f"Traject {count}: {traject}")
        print()
    return traject_list

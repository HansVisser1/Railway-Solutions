import csv

def output_to_csv(best_trajects, quality, traject_type='test', network='test', iterations='test'):
    """
    This function converts the output to the right format and stores it in a csv file.
    """
    # make writer
    with open(f"Results/{iterations}_iterations_{traject_type}_{network}.csv", 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['train', 'stations'])

        # make the correct format from the best trajects
        count = 1
        for traject in best_trajects:
            stations = []
            for connection in traject:
                if connection[0] not in stations:
                    stations.append(connection[0])
                if connection[1] not in stations:
                    stations.append(connection[1])

            # write to csv
            writer.writerow([f"train_{count}", f'"{stations}"'])
            count += 1
        writer.writerow(['score', quality])

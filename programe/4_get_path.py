import pandas as pd

path_df = pd.read_csv('middle_data/4_49_mission_distance.csv', header=None, index_col=False)
# mission
from_list = [0, 0, 0, 0]
last = [0, 0, 0, 0]
for mission_index in range(49):
    review_list = ['FH01', 'FH03', 'FH10', 'FH12']
    series_1 = path_df.iloc[[0 + mission_index * 4],]
    series_3 = path_df.iloc[[1 + mission_index * 4],]
    series10 = path_df.iloc[[2 + mission_index * 4],]
    series12 = path_df.iloc[[3 + mission_index * 4],]
    series_list = [series_1, series_3, series10, series12]
    distance_matrix = []
    # Get all distence
    for series in series_list:
        d_series = []
        for to_i in range(4):
            d_t = int(series[0] + series[4 + to_i])
            d_series.append(d_t)
        distance_matrix.append(d_series)
    # Find min distance and from which to which
    min_distance_list = []
    min_distance_index = []
    for distance in distance_matrix:
        min_distance = min(distance)
        min_index = distance.index(min_distance)
        min_distance_list.append(min_distance)
        min_distance_index.append(min_index)
    # 全局最短路径
    global_min = min(min_distance_list)
    global_from = min_distance_list.index(global_min)
    global_to = min_distance_index[global_from]
    from_list[global_from] += 1
    last[global_to] += 1
    with open('4_distribution.csv', 'a') as f:
        f.write("Mission " + str(mission_index + 1) + "," + review_list[global_from] +
                "," + review_list[global_to] + "," + str(global_min) + "," + str(
            series_list[global_from][2].values.tolist()[0]))
        f.write('\t\n')

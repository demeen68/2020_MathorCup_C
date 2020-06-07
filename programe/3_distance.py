import pandas as pd
import copy
from utils.tsp_2 import tsp_quick


def get_mission_path(mission_df: pd.DataFrame, ):
    def get_distance(dis_from: str, dis_to, type_to=0):
        if type_to == 0:
            # type_to = 0 : distance between lattice and lattice
            d_frome = int(all_store_index[all_store_index.values == dis_from].index[0])
            d_to = int(all_store_index[all_store_index.values == dis_to].index[0])
            data = distance_df.iloc[[d_frome], [d_to]].values.tolist()[0][0]
            return data
        elif type_to == 1:
            # distance between lattice and review
            d_frome = int(all_store_index[all_store_index.values == dis_from].index[0])
            dis_to_index = 2999 + int(dis_to)
            data = int(distance_df.iloc[[d_frome], [dis_to_index]].values.tolist()[0][0])
            return data

    def get_lattice_matrix():
        distance_matrix = []
        for index_from, mission_from in mission_df.iterrows():
            order_from = mission_from['商品货格']
            distance_matrix_sub = []
            for index_to, mission_to in mission_df.iterrows():
                order_to = mission_to['商品货格']
                distance = get_distance(order_from, order_to)
                distance_matrix_sub.append(distance)
                pass
            distance_matrix.append(distance_matrix_sub)
        return distance_matrix

    def add_review_distance(distance_matrix: list, review_name):
        """
        对距离矩阵二次添加,添加复核台与每个点的距离,构成包含货格与货格和货格与一个复核台距离的大矩阵
        :param distance_matrix: 货格与货格之间距离的矩阵
        :param review_name: 复核台编号
        :return: 返回包含了一个复核台的距离矩阵
        """
        review_name = int(review_name[-2:])
        matrix = []
        for index_from, mission_from in mission_df.iterrows():
            order_from = mission_from['商品货格']
            distance = get_distance(order_from, review_name, 1)
            matrix.append(distance)
        matrix_2 = copy.copy(matrix)
        distance_matrix.append(matrix_2)
        matrix.append(0)
        for i, mx in enumerate(distance_matrix):
            mx.append(matrix[i])

        return distance_matrix

    start_index = len(mission_df)
    distance_matrix = get_lattice_matrix()
    distance_matrix_addition = add_review_distance(copy.copy(distance_matrix), init_review)
    # (FH03，FH11)
    sum_distance, node_path = tsp_quick(distance_matrix_addition, start_index)
    last_lattice = mission_df.iloc[node_path[-1]]['商品货格']
    d03 = get_distance(last_lattice, 3, 1)
    d11 = get_distance(last_lattice, 11, 1)
    if d03 > d11:
        sum_distance += d11
        node_path.append('FH11')
    else:
        sum_distance += d03
        node_path.append('FH03')
    return sum_distance, node_path


all_mission = ['T0002', 'T0003', 'T0004', 'T0005', 'T0006']
all_mission_df = pd.read_excel('data/store_data.xlsx', sheet_name='任务单')
all_store_index = pd.read_excel('data/store_data.xlsx', sheet_name='货格')['货格名称']
distance_df = pd.read_csv('data/distance_data.csv', header=None, index_col=False)
init_review = 'FH03'
for mission in all_mission:
    target_mission = all_mission_df[all_mission_df['任务单号'] == mission]
    sum_distance, node_path = get_mission_path(target_mission)
    with open('middle_data/3_all_mission_distance.csv', 'a') as f:
        f.write(str(sum_distance) + ',' + init_review + ',' + str(node_path[1:-1])[1:-1] + ',' + node_path[-1])
        f.write('\t\n')
    init_review = node_path[-1]

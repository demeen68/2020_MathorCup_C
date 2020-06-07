import pandas as pd
import copy
from utils.tsp_2 import tsp_quick


def get_mission_path(mission_df: pd.DataFrame):
    """
    TSP问题,获得执行完整的任务单的最短路径
    :param mission_df: 当前任务单的信息
    :return: 返回当前任务单的最优路径
    """

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

    # 对距离矩阵二次添加,添加复核台与每个点的距离
    def add_review_distance(distance_matrix: list, review_name):
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

    all_store_index = pd.read_excel('data/store_data.xlsx', sheet_name='货格')['货格名称']
    distance_df = pd.read_csv('data/distance_data.csv', header=None, index_col=False)
    distance_matrix = get_lattice_matrix()
    distance_matrix_addition = add_review_distance(copy.copy(distance_matrix), "FH10")
    return tsp_quick(distance_matrix_addition, 23)


mission_df = pd.read_excel('data/store_data.xlsx', sheet_name='任务单')
mission_df = mission_df[mission_df['任务单号'] == 'T0001']

sum_distance, node_path = get_mission_path(mission_df)

import pandas as pd
import copy
from utils.tsp_2 import tsp_quick


def get_mission_path(mission_df: pd.DataFrame, init_review):
    # 获得任务单最短路径
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

    start_index = len(mission_df)
    distance_matrix = get_lattice_matrix()
    distance_matrix_addition = add_review_distance(copy.copy(distance_matrix), init_review)
    sum_distance, node_path = tsp_quick(distance_matrix_addition, start_index)
    last_lattice = mission_df.iloc[node_path[-1]]['商品货格']
    # 'FH01', 'FH03', 'FH10', 'FH12'
    d01 = get_distance(last_lattice, 1, 1)
    d03 = get_distance(last_lattice, 3, 1)
    d10 = get_distance(last_lattice, 10, 1)
    d12 = get_distance(last_lattice, 12, 1)
    dmin = min(d01, d03, d10, d12)
    # 最后一个复核台的选择
    d_all = [d01, d03, d10, d12]
    index_command = capable_review[d_all.index(dmin)]
    return sum_distance, node_path, d_all, index_command


all_mission = ['T0001', 'T0002', 'T0003', 'T0004', 'T0005', 'T0006', 'T0007', 'T0008', 'T0009', 'T0010', 'T0011',
               'T0012', 'T0013', 'T0014', 'T0015', 'T0016', 'T0017', 'T0018', 'T0019', 'T0020', 'T0021', 'T0022',
               'T0023', 'T0024', 'T0025', 'T0026', 'T0027', 'T0028', 'T0029', 'T0030', 'T0031', 'T0032', 'T0033',
               'T0034', 'T0035', 'T0036', 'T0037', 'T0038', 'T0039', 'T0040', 'T0041', 'T0042', 'T0043', 'T0044',
               'T0045', 'T0046', 'T0047', 'T0048', 'T0049', ]
capable_review = ['FH01', 'FH03', 'FH10', 'FH12']
all_mission_df = pd.read_excel('data/store_data.xlsx', sheet_name='任务单')
all_store_index = pd.read_excel('data/store_data.xlsx', sheet_name='货格')['货格名称']
distance_df = pd.read_csv('data/distance_data.csv', header=None, index_col=False)
for mission in all_mission:
    target_mission = all_mission_df[all_mission_df['任务单号'] == mission]
    for init_review in capable_review:
        sum_distance, node_path, d_allF, index_command = get_mission_path(target_mission, init_review)
        with open('middle_data/4_49_mission_distance.csv', 'a') as f:
            f.write(
                str(sum_distance) + ',' + init_review + ',' + str(node_path[1:]).replace(',', '-')
                + ',' + index_command + ',' + str(d_allF))
            f.write('\t\n')

def tsp_quick(dist, start_index):
    """
    TSP问题贪心算法求解
    :param dist: 距离矩阵
    :param start_index: 起点
    :return:
    """
    n = len(dist)
    sum_distance = 0
    seq_result = []
    seq_result.append(0)
    i = 1
    j = 0
    while True:
        k = 1
        Detemp = 10000000
        while True:
            l = 0
            flag = 0
            if k in seq_result:
                flag = 1
            if (flag == 0) and (dist[k][seq_result[i - 1]] < Detemp):
                j = k
                Detemp = dist[k][seq_result[i - 1]]
            k += 1
            if k >= n:
                break
        seq_result.append(j)
        i += 1
        sum_distance += Detemp
        if i >= n:
            break
    sum_distance += dist[0][j]
    sum_distance -= dist[0][start_index]  # 这里不要计算从最后一个点到起点的距离,为了后续方便计算
    start_index = seq_result.index(start_index)
    node_list = seq_result[start_index:] + seq_result[:start_index]
    return sum_distance, node_list

import pandas as pd
import numpy as np


def num_to_vec(w: int):
    """
    为了方便计算,我们把S001定义为(1,1),S002定义为(2,1),S003定义为(1,2)...S009为(3,1)
    :param w: 货柜的官方编号
    :return: 本组自定义的编号
    """
    if w % 8 != 0:
        x = (w // 8 + 1) * 2 - w % 2
        if w % 2 != 0:
            w += 1
        if w % 8 == 0:
            y = 4
        else:
            y = w % 8 // 2
        return x, y
    else:
        x = w // 8 * 2
        y = 4
        return x, y


def lattice_distance():
    def get_data(x, y, z, a, b, c):
        """
        get distance from (x,y,z) to (a,b,c)
        :param x:起始点横坐标
        :param y:起始点纵坐标
        :param z:起始货柜的货格编号,从下到上依次是1,2....15
        :param a:终止点横坐标
        :param b:终止点纵坐标
        :param c:终止点的货格编号
        """

        def only_y_equal_dx():
            dx = None
            if diff_x == 1:
                dx = 1500 * 2 + 800 * 2
            elif diff_x % 2 == 0:
                dx = diff_x // 2 * (800 * 2 + 1500) + 750 + 750
            elif diff_x % 2 != 0:
                if x % 2 == 0:
                    dx = diff_x // 2 * (800 * 2 + 1500) + 1500
                elif x % 2 != 0:
                    dx = diff_x // 2 * (800 * 2 + 1500) + 1500 * 2 + 800 * 2
            return dx

        def only_x_equal_dy():
            if diff_y == 0:
                return 0
            dy = diff_y * 2000 + ((y - b) // diff_y * (z - c) + 15) * 800
            return dy

        diff_x = np.abs(x - a)
        diff_y = np.abs(y - b)
        diff_z = np.abs(z - c)
        if x == a and y == b and c == z:
            return 0
        if diff_x == 1 and max(a, x) % 2 == 1 and diff_y != 0:
            dx = 1500
            dy = only_x_equal_dy()
            return dx + dy

        if x == a and y == b:  # x相同,y相同
            dx = 1500
            dy = diff_z * 800
            return dx + dy
        elif y == b:  # x不同,y相同
            dy = 800 * max(z + c, 30 - z - c) + 1500
            dx = only_y_equal_dx()
            return dx + dy
        elif x == a:  # x相同,y不同
            dx = 1500
            dy = only_x_equal_dy()
            return dx + dy
        else:
            dx = only_y_equal_dx()
            dy = only_x_equal_dy()
            return dx + dy

    review_data = pd.read_excel('data/store_data.xlsx', sheet_name='货格')
    all_names = review_data['货格名称']
    for name_from in all_names:
        x, y = num_to_vec(int(name_from[1:4]))
        z = int(name_from[4:])
        for name_to in all_names:
            a, b = num_to_vec(int(name_to[1:4]))
            c = int(name_to[4:])
            # get_data(x,y,z,a,b,c)
            data = get_data(x, y, z, a, b, c)
            with open('distance.csv', 'a') as f:
                f.write(str(data) + ',')
        with open('distance.csv', 'a') as f:
            f.write('\t\n')


def review_lattice():
    """
    计算货格与复核台之间的距离
    """

    def check_type(data):
        type = data['所属货架']
        type_int = int(type[-1])
        if type_int % 2 == 0:
            return 0
        else:
            return 1

    review_data = pd.read_excel('data/store_data.xlsx', sheet_name='货格')
    lattice_df = pd.read_excel('data/store_data.xlsx', sheet_name='复核台')
    # type = 1 表示左边 ; type = 0 表示右边
    review_data['type'] = review_data.apply(check_type, axis=1)
    for i, lattice_row in lattice_df.iterrows():
        # ['复核台名称', '坐标 x,毫米', '坐标 y,毫米', '复核台长,毫米', '复核台宽,毫米']
        x = lattice_row['坐标 x,毫米']
        y = lattice_row['坐标 y,毫米']
        if int(lattice_row['坐标 x,毫米']) == 0:  # left
            for i, review_row in review_data.iterrows():
                a = review_row['坐标 x,毫米']
                b = review_row['坐标 y,毫米']
                if review_row['type'] == 0:
                    distance = a + abs(b - y) - 500 + +750 * 2
                else:
                    distance = a + abs(y - b) - 500
                with open('review_lattice.csv', 'a') as f:
                    f.write(str(distance) + ',')
        else:  # bottom
            x = lattice_row['坐标 x,毫米']
            for i, review_row in review_data.iterrows():
                a = review_row['坐标 x,毫米']
                b = review_row['坐标 y,毫米']
                if (a < x and review_row['type'] == 1) or (a > x and review_row['type'] == 0):
                    distance = abs(a - x) + b - 500 + 750 * 2
                else:
                    distance = abs(a - x) + b - 500
                with open('review_lattice.csv', 'a') as f:
                    f.write(str(distance) + ',')
            pass
        with open('review_lattice.csv', 'a') as f:
            f.write('\t\n')
    review_df = pd.read_csv('review_lattice.csv')
    review_df = review_df.T
    review_df.to_csv('review_lattice_T.csv', header=None)


def review_review():
    """
    货柜货柜的距离
    """
    lattice_df = pd.read_excel('data/store_data.xlsx', sheet_name='复核台')
    for i, lattice_row in lattice_df.iterrows():
        x = lattice_row['坐标 x,毫米']
        y = lattice_row['坐标 y,毫米']
        for j, la2_row in lattice_df.iterrows():
            a = la2_row['坐标 x,毫米']
            b = la2_row['坐标 y,毫米']
            data = abs(x - a) + abs(y - b)
            with open('middle_data/review_review.csv', 'a') as f:
                f.write(str(data) + ',')
        with open('middle_data/review_review.csv', 'a') as f:
            f.write('\t\n')

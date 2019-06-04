# -*- coding:utf-8 -*-
import csv
import os

import distances
import pandas as pd
from point import Point
from read_data import read

'''
TD-TR算法，误差度量是SED(时间同步距离）
'''


# DP algorithm
def dp_compress(points, feature_points, max_value):
    start_index = 0
    end_index = len(points) - 1
    if start_index < end_index:
        index = start_index + 1
        max_vertical_distance = 0
        key_point_index = 0
        while index < end_index:
            curr_distance = distances.sed_distance(points[start_index], points[index], points[end_index])
            if curr_distance >= max_vertical_distance:
                max_vertical_distance = curr_distance
                key_point_index = index
            index = index + 1
        if max_vertical_distance >= max_value:
            feature_points.append(points[key_point_index])
            dp_compress(points[start_index:key_point_index + 1], feature_points, max_value)
            dp_compress(points[key_point_index:end_index + 1], feature_points, max_value)


# 轨迹划分
def trajectory_partition(points):
    feature_points = []
    feature_points.append(points[0])
    feature_points.append(points[-1])
    import time
    start = time.clock()
    dp_compress(points, feature_points, 6)
    end = time.clock()
    feature_points = sorted(feature_points, key=lambda x: x[2])
    return feature_points, end - start


# -------------------------------------------------------------------------------
if __name__ == '__main__':
    # 文件路径
    path = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data_4.0\0"
    # 文件保存路径
    save_dir = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\TDTRFeature_Trajectory\0"
    time_path = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Time\TDTRtime0.csv"
    size_path = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\NumberPoints\TDTR0.csv"
    file_list = os.listdir(path)
    # 按时间顺序读取文件
    file_list.sort(key=lambda fn: os.path.getatime(path + "\\" + fn))
    data_list = []
    time_set = []  # 记录每个轨迹划分的时间
    size_set = []  # 记录每个划分后轨迹的大小
    points = []  # 所以轨迹数据点
    total_time = 0  # 记录总的划分时间
    id = 0
    for i in range(len(file_list)):
        data_list.append(path, read(file_list[i]))
    for j in range(len(data_list)):
        for point in data_list[j]:
            p = Point(id, point[0], point[1], point[2])
            points.append(p)
            id += 1
        feature_data, time = trajectory_partition(points)
        total_time += time
        time_set.append(time)
        size_set.append(len(feature_data))
        filename = "Trajectory" + str(j + 1) + ".csv"
        file_path = os.path.join(save_dir, fileName)
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in feature_data:
                writer.writerow(row)

    dataframe1 = pd.DataFrame({'time': time_set})
    dataframe1.to_csv(time_path, index=False)

    dataframe2 = pd.DataFrame({'Number': size_set})
    dataframe2.to_csv(size_path, index=False)

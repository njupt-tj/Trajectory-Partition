# -*- coding:utf-8 -*-
import csv
import math
import os

import numpy as np


# tarjectory partition
# --------------------------------------------------------------------------------
# version 1.0
# 计算两个时间戳的间隔（秒）
def calculate_interval(t1, t2):
    import datetime
    s1 = '2018-3-22' + ' ' + t1
    s2 = '2018-3-22' + ' ' + t2
    # 字符串转时间格式
    d1 = datetime.datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(s2, '%Y-%m-%d %H:%M:%S')
    return (d2 - d1).total_seconds()


# 计算点之间的距离
def calculate_distance(x, y):
    return np.sqrt(np.sum(np.square(x - y))) * 1000


# 保存未原始的特征点到文件中
def Save_feature_point(point_index):
    # print(point_index)
    prim_Trajectory = open(
        r'C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data\000\Trajectory\20081023025304.txt')
    # Trajectory_list=os.listdir(prim_Trajectory_path)
    LLT = []
    ALL_LLT = []
    for line in prim_Trajectory.readlines():
        if line.__len__() > 50:
            LLT.append(float(line.split(',')[0]))
            LLT.append(float(line.split(',')[1]))
            LLT.append(line.split(',')[-1].strip())
            ALL_LLT.append(LLT)
            LLT = []
    # print(ALL_LLT)
    feature_Trajectory = r'C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Feature_Trajectory\0\feature_trajectory1.csv'
    feature_Trajectory_list = []
    for i in list(point_index):
        # print(i)
        feature_Trajectory_list.append(ALL_LLT[i])
    with open(feature_Trajectory, 'w', newline='') as f:
        writer = csv.writer(f)
        for item in feature_Trajectory_list:
            writer.writerow(item)


# 读取数据并转换类型
def readData(trajectory):
    file = os.path.join(trajectory_path, trajectory)
    # Feature_point = []  # 特征点集合
    Data_list = []
    # 读取数据文件，并保存到Data_list
    with open(file, 'r') as f:
        data_list = csv.reader(f)
        for row in data_list:
            Data_list.append(row)

    # Data_list将集合里的字符串类型转换成数值类型
    for point in Data_list:
        point[0] = float(point[0])
        point[1] = float(point[1])
    return Data_list


# 两个坐标之间的距离
def distance(P1, P2):
    x = np.array(P1[:2])
    y = np.array(P2[:2])
    return np.sqrt(np.sum(np.square(x - y))) * 1000


# 一个簇的中心点
def mean_Coordinate1(Cluster):
    N = len(Cluster)
    mean_P = []
    sum_x = 0
    sum_y = 0
    for i in range(N):
        sum_x = sum_x + Cluster[i][0]
        sum_y = sum_y + Cluster[i][1]
    mean_P.append(sum_x / N)
    mean_P.append(sum_y / N)
    mean_P.append(Cluster[0][2])
    mean_P.append(Cluster[N - 1][2])
    return mean_P


# 两个点之间的平均坐标
def mean_Coordinate2(P1, P2):
    mean_P = []
    mean_P.append((p1[0] + p2[0]) / 2)
    mean_p.append((p1[1] + p2[1]) / 2)
    mean_P.append(P1[2])
    mean_P.append(P2[2])
    return mean_P


# 一个簇的持续时长
def duration1(Cluster):
    t1 = Cluster[0][2]
    t2 = Cluster[len(Cluster) - 1][2]
    return calculate_interval(t1, t2)


# 两个点之间的时间间隔
def duration2(P1, P2):
    t1 = P1[2]
    t2 = p1[2]
    return calculate_interval(t1, t2)


# 合并两个簇
def merge(Cluster, PreviousC):
    for item in Cluster:
        PreviousC.append(item)
    return PreviousC


# add a cluster to SP
def add(Cluster, Previous, SP):
    mean_P = mean_Coordinate1(Cluster)
    if distance(mean_P, SP[-1]) < d:
        Previous = merge(Cluster, Previous)
    else:
        SP.append(mean_P)
        Previous = Cluster
        Cluster = []


def check(Cluster, PreviousC, SP, P):
    currentC_P = mean_Coordinate1(Cluster)
    preC_P = mean_Coordinate1(PreviousC)
    if duration(preC_P, currentC_P) < t and distance(preC_P, currentC_P) < d:
        PreviousC = merge(Cluster, PreviousC)
        meanP = mean_Coordinate1(PreviousC)
        if distance(meanP, P) > d and duration(PreviousC) > t:
            add(PreviousC, SP)
        else:
            PreviousC = Cluster
            Cluster = []


def calculate_D(D, x, y, z):
    xA = np.array(D[x][:2])
    yA = np.array(D[y][:2])
    zA = np.array(D[z][:2])
    x_y_distance = calculate_distance(xA, yA)
    x_z_distance = calculate_distance(xA, zA)
    z_y_distance = calculate_distance(zA, yA)
    if x_z_distance == 0:
        return x_y_distance
    elif x_y_distance == 0 or z_y_distance == 0:
        return 0
    else:
        p = (x_y_distance + x_z_distance + z_y_distance) / 2
        S = math.sqrt(math.fabs(p * (p - x_y_distance) * (p - x_z_distance) * (p - z_y_distance)))
        return (2 * S) / x_z_distance


def extraction_SP(T):
    """TDBC停留点提取"""
    SP = []
    PreviousC = []
    Cluster = []  # 当前簇
    # 第一种类型停留点
    if calculate_distance(np.array(T[0][:2]), np.array(T[len(T) - 1][:2])) < d:
        SP.append(T[0])
    for i in range(len(T)):
        # 第二种类型停留点
        Cluster.append(T[i])
        meanP = mean_Coordinate1(Cluster)
        if distance(meanP, T[i]) < d:
            Cluster.append(T[i])
            continue
        if distance(meanP, T[i]) > d and duration1(Cluster) > t:
            add(Cluster, SP)
            continue
        if distance(meanP, T[i]) > d and duration1(Cluster) < t:
            check(Cluster, PreviousC, SP, T[i])
            continue
        # 第三种类型停留点
        if distance(T[i - 1], T[i]) < d and duration2(T[i - 1], T[i]) > t:
            SP.append(mean_Coordinate2(T[i - 1], T[i]))
            continue
        if distance(T[i - 1], T[i]) > d and duration2(T[i - 1], T[i]) > t:
            continue
    return SP


def direction_DP(D, FP, th):
    start_index = 0
    end_index = len(D) - 1
    index = 0
    if start_index < end_index:
        indx = start_index + 1
        max_value = 0
        key_index = 0
        while index < end_index:
            # 计算最大方向值
            dis = calculate_D(D, start_index, index, end_index)
            if dis >= max_value:
                max_value = dis
                key_index = index
            index = index + 1
        if max_value >= th:
            FP.append(D[key_index])
            direction_DP(D[start_index:key_index + 1], FP, th)
            direction_DP(D[key_index:end_index + 1], FP, th)


# ----------------------------------------------------------------------------------------------
# 轨迹划分
def trajectory_partition(Data_list, SP):
    '''基于停留点的DP算法'''
    Index = []
    for item in SP:
        Index.append(Data_list.index(item))
    FP = []
    E_th = 25
    import time
    start = time.clock()
    while s < len(Index) - 1:
        direction_DP(Data_list[Index[s]:Index[s + 1] + 1], FP, E_th)
        s = s + 1
    end = time.clock()
    return FP, end - start


# -------------------------------------------------------------------------------
# 划分单个轨迹
if __name__ == '__main__':
    trajectory_path = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data_4.0\0"
    trajectory_list = os.listdir(trajectory_path)
    # 按时间顺序读取文件
    trajectory_list.sort(key=lambda fn: os.path.getatime(trajectory_path + "\\" + fn))
    Data_list = []
    for i in range(len(trajectory_list)):
        Data_list.append(readData(trajectory_list[i]))
    t = 500
    d = 60
    SP = extraction_SP(Data_list[0])
    print(len(SP))
    # Feature_points, time = trajectory_partition(T, SP)
    # print(len(Feature_points))
    # 原始点（包含特征点）写入文件
    with open('Raw_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in Raw_points:
            writer.writerow(row)
    # 特征点写入到到文件
    with open('Feature_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in Feature_points:
            writer.writerow(row)

# -*- coding:utf-8 -*-
import csv
import math
import os
from decimal import Decimal
import cProfile
import numpy as np

# tarjectory partition
# --------------------------------------------------------------------------------
# version 1.0
# 计算两个时间戳的间隔（秒）
def calculate_interval(t1, t2):
    import datetime
    s1 = '%s %s' % ('2018-3-22', t1)
    s2 = '%s %s' % ('2018-3-22', t2)
    # 字符串转时间格式
    d1 = datetime.datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(s2, '%Y-%m-%d %H:%M:%S')
    return (d2 - d1).total_seconds()


# 计算点之间的距离
def calculate_distance(x, y):
    return np.sqrt(np.sum(np.square(x - y))) * 1000


# 计算轨迹段的移动速度
def calculate_speed(xy_distance, t1, t2):
    xy_time = calculate_interval(t1, t2)
    return xy_distance / xy_time


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
    file = os.path.join(trajectoryPath, trajectory)
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


# 后向搜索
def Backward_search(D, x, d):
    i1 = x
    key1 = 0
    while i1 > 0:
        if calculate_distance(np.array(D[x][:2]), np.array(D[i1 - 1][:2])) > d:
            key1 = i1
            break
        i1 = i1 - 1
    return key1


# 前向搜索
def Forward_search(D, x, d):
    i2 = x
    key2 = 0
    while i2 < len(D) - 1:
        if calculate_distance(np.array(D[x][:2]), np.array(D[i2 + 1][:2])) > d:
            key2 = i2
            break
        i2 = i2 + 1
    if key2 == 0 or i2 == len(D) - 1:
        return i2
    else:
        return key2


# 去除冗余的点
def Remove_rdy(D, x, y):
    del D[x:y + 1]


# 计算方向角和垂直距离
def calculate_AD(D, x, y, z):
    x1 = np.array(D[x][:2])
    y1 = np.array(D[y][:2])
    z1 = np.array(D[z][:2])

    x_y = y1 - x1
    x_z = z1 - x1
    z_y = y1 - z1
    x_y_distance = np.sqrt(np.sum(np.square(x_y)))
    x_z_distance = np.sqrt(np.sum(np.square(x_z)))
    z_y_distance = np.sqrt(np.sum(np.square(z_y)))
    if x_y_distance == 0 or z_y_distance == 0:
        k1 = 0
        k2 = 0
        per_d = 0
    else:
        k1 = Decimal(str(np.dot(x_y, x_z))) / Decimal(str(x_y_distance * x_z_distance))
        per_d = x_y_distance * 1000 * math.sin(math.acos(k1))
        z_x = -1 * x_z
        k2 = Decimal(str(np.dot(z_x, z_y))) / Decimal(str(z_y_distance * x_z_distance))

    return max(math.acos(k1), math.acos(k2)), per_d


def Remove_duplicates(FP):
    A = []
    [A.append(x) for x in FP if not x in A]
    return A


def direction_DP(D, FP, th):
    start_index = 0
    end_index = len(D) - 1
    if start_index < end_index:
        index = start_index + 1
        max_value = 0
        key_index = 0
        while index < end_index:
            # 计算最大方向值
            Angle, dis = calculate_AD(D, start_index, index, end_index)
            current_value = np.sin(Angle) * dis
            if current_value >= max_value:
                max_value = current_value
                key_index = index
            index = index + 1
        if max_value >= th:
            FP.append(D[key_index])
            direction_DP(D[start_index:key_index + 1], FP, th)
            direction_DP(D[key_index:end_index + 1], FP, th)


# ----------------------------------------------------------------------------------------------
# 轨迹划分
def trajectory_Partition(Data_list):
    '''基于用户移动特征划分轨迹'''

    FP = []  # 存储特征点
    n = len(Data_list)
    import copy
    Data_list_copy = copy.copy(Data_list)
    # 将第一个点加入到特征集合中
    FP.append(Data_list[0])
    # 将最后一个点加入到特征集合中
    FP.append(Data_list[n - 1])
    # 基于速度划分
    i = 0
    V = []
      # 速度改变较大的点集合
    while i < n - 1:
        dis = calculate_distance(np.array(Data_list[i][:2]), np.array(Data_list[i + 1][:2]))
        v = calculate_speed(dis, Data_list[i][2], Data_list[i + 1][2])
        V.append(v)
        i = i + 1
    # 可视化
    # import matplotlib.pyplot as plt
    # X=np.arange(1,len(V)+1)
    # plt.plot(X, V)
    # plt.show()
    avg_v = np.mean(np.array(V))  # 计算速度均值
    Sum = 0
    for item in V:
        Sum = Sum + (item - avg_v) * (item - avg_v)
    v_th = math.sqrt(Sum / len(V))  # 以标准差作为速度阈值
    j = 0
    VP = []
    # 根据速度阈值寻找关键点
    while j < len(V) - 1:
        if abs(V[j + 1] - V[j]) >= v_th:
            VP.append(Data_list[j + 1])
        j = j + 1

    # ----------------------------------------------------------------------------
    # 基于停留点划分
    k = 0
    # 设定阈值
    t_th = 4 * 60
    v_thr = 0.6
    d_th =20
    SP = []  # 停留点集合
    while k < len(Data_list) - 1:
        if V[k] is 0 or V[k] <= v_thr:
            k1 = Backward_search(Data_list, k + 1, d_th)
            k2 = Forward_search(Data_list, k + 1, d_th)
            T = calculate_interval(Data_list[k1][2], Data_list[k2][2])
            if T >= t_th:
                kp = round((k1 + k2) / 2)
                SP.append(Data_list[kp])
                # 去除区域内冗余的点,防止重复计算
                Remove_rdy(Data_list, k1, k2)
                k = k1
            else:
                k = k + 1
        else:
            k = k + 1
    # -----------------------------------------------------------------------------
    print(len(SP))
    [FP.append(x) for x in VP]
    [FP.append(y) for y in SP]
    # 去除FP中可能重复的特征点
    FPs = Remove_duplicates(FP)
    # 按时间先后顺序重新排序
    FP = sorted(FPs, key=lambda x: x[2])
    for item in FP:
        if not item in Data_list:
            Data_list.append(item)
    Data_list = sorted(Data_list, key=lambda x: x[2])
    Index = []
    for item in FP:
        Index.append(Data_list.index(item))
    # 基于方向的DP划分

    s = 0
    E_th =  10  * math.pi / 6
    import time
    start = time.clock()
    while s < len(Index) - 1:
        direction_DP(Data_list[Index[s]:Index[s + 1] + 1], FP, E_th)
        s = s + 1
    end = time.clock()
    # 按时间先后顺序重新排序
    sorted_FP = sorted(FP, key=lambda x: x[2])
    # --------------------------------------------------------------------------------
    # for item in FP:
    #     if item in Data_list_copy:
    #         points_index.append(Data_list_copy.index(item))
    # Save_feature_point(points_index)
    return Data_list, sorted_FP, end-start


# -------------------------------------------------------------------------------
# 划分单个轨迹
if __name__ == '__main__':
    trajectoryPath = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data_4.0\0"
    trajectoryList = os.listdir(trajectoryPath)
    # 按时间顺序读取文件
    trajectoryList.sort(key=lambda fn: os.path.getatime(trajectoryPath + "\\" + fn))
    Data_list = []
    for i in range(len(trajectoryList)):
        Data_list.append(readData(trajectoryList[i]))
    # import pandas as pd
    # path1 = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Rawtra\9"
    # path2 = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Feature_Trajectory1\9"
    # Time=[]
    # Number=[]
    # for j in range(len(Data_list)):
    Raw_data, Feature_data , time= trajectory_Partition(Data_list[47])
    print(len(Feature_data))
    #     Time.append(time)
    #     Number.append(len(Feature_data))
    #     fileName = "Trajectory" + str(j + 1) + ".csv"
    #     filePath1 = os.path.join(path1, fileName)
    #     filePath2 = os.path.join(path2, fileName)
    #     with open(filePath1, 'w', newline='') as f:
    #         writer = csv.writer(f)
    #         for row in Raw_data:
    #             writer.writerow(row)
    #     with open(filePath2, 'w', newline='') as f:
    #         writer = csv.writer(f)
    #         for row in Feature_data:
    #             writer.writerow(row)
    #
    # path3 = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Time\time9.csv"
    # path4 = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\NumberPoints\9.csv"
    #
    # dataframe1=pd.DataFrame({'time':Time})
    # dataframe1.to_csv(path3, index=False)
    #
    # dataframe2=pd.DataFrame({'Number':Number})
    # dataframe2.to_csv(path4, index=False)
    # with open(path3, 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(Time)
        # for row in Time:
        #     writer.writerow(round(row,2))

    # with open(path4, 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     for row in Number:
    #         writer.writerow(row)

    # tra_Data = readData(trajectoryList[47])
    # print(len(tra_Data))
    # cProfile.run("trajectory_Partition(tra_Data)")
    # raw_Points, feature_Points = trajectory_Partition(tra_Data)
    # print(len(feature_Points))
    # 原始点（包含特征点）写入文件
    with open('Raw_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in Raw_data:
            writer.writerow(row)
    # 特征点写入到到文件
    with open('Feature_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in Feature_data:
            writer.writerow(row)

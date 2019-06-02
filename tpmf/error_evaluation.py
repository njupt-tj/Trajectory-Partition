# -*- coding:utf-8 -*-
import csv
import math
import os
from decimal import Decimal

import numpy as np


# Raw_file='Raw_data.csv'
# Feature_file='Feature_data.csv'

# -------------------------------------------------------------------------------------------------------
def calculate_angle(x, y, z):
    x_y = y - x
    x_z = z - x
    xy_distance = np.sqrt(np.sum(np.square(y - x)))
    # yz_distance = np.sqrt(np.sum(np.square(y - z)))
    xz_distance = np.sqrt(np.sum(np.square(z - x)))
    if xz_distance == 0:
        return 0
    else:
        k = Decimal(str(np.dot(x_y, x_z))) / Decimal(str(xy_distance * xz_distance))
        # k=(xy_distance*xy_distance+xz_distance*xz_distance-yz_distance*yz_distance)/(2*xy_distance*xz_distance)
        if k>1:
            k=1
        elif k<-1:
            k=-1
        return math.acos(float(k))


def F_MaxA(Raw_data, start, end):
    a = np.array(Raw_data[start])
    b = np.array(Raw_data[end])
    Max_A = 0
    while start < end:
        c = np.array(Raw_data[start + 1])
        Angle = calculate_angle(a, b, c)
        if Angle > Max_A:
            Max_A = Angle
        start = start + 1

    return Max_A


def B_MaxA(Raw_data, end, start):
    a = np.array(Raw_data[start])
    b = np.array(Raw_data[end])
    Max_A = 0
    while end > start:
        c = np.array(Raw_data[end - 1])
        Angle = calculate_angle(b, a, c)
        if Angle > Max_A:
            Max_A = Angle
        end = end - 1

    return Max_A


def Calculate_distance(Raw_data, start, end, Distance):
    a = np.array(Raw_data[start])
    b = np.array(Raw_data[end])
    ab_distance = np.sqrt(np.sum(np.square(a - b))) * 1000
    while start < end:
        c = np.array(Raw_data[start + 1])
        ac_distance = np.sqrt(np.sum(np.square(c - a))) * 1000
        cb_distance = np.sqrt(np.sum(np.square(b - c))) * 1000
        p = (ab_distance + ac_distance + cb_distance) / 2
        S = math.sqrt(math.fabs(p * (p - ab_distance) * (p - ac_distance) * (p - cb_distance)))
        d = (2 * S) / ab_distance
        Distance.append(d)
        start = start + 1


# ---------------------------------------------------------------------------------------------------------
# 特征数据在原始数据中的索引
def Error_start(Raw_file, Feature_file):
    Raw_data = []
    with open(Raw_file, 'r') as R:
        reader_list = csv.reader(R)
        for item in reader_list:
            Raw_data.append(item[0:2])

    # 读取特征数据
    Feature_data = []
    with open(Feature_file, 'r') as F:
        reader_list = csv.reader(F)
        for item in reader_list:
            Feature_data.append(item[0:2])

    # 将数组字符串元素转换为float类型
    for item in Raw_data:
        item[0] = float(item[0])
        item[1] = float(item[1])

    for item in Feature_data:
        item[0] = float(item[0])
        item[1] = float(item[1])

    Index = []
    for item in Feature_data:
        if item in Raw_data:
            Index.append(Raw_data.index(item))
        else:
            print('no such item')

    # 计算简化后的轨迹与原始轨迹的误差
    Angle = []
    Distance = []
    for i in range(len(Index) - 1):
        if len(Raw_data[Index[i]:Index[i + 1]]) == 2:
            Angle.append(0)
            Distance.append(0)
        else:
            start = Index[i]
            end = Index[i + 1]
            # 计算前向和后向最大方向的平均
            Forward_maxA = F_MaxA(Raw_data, start, end)
            Backward_maxA = B_MaxA(Raw_data, end, start)
            Angle.append((Forward_maxA + Backward_maxA) / 2)
            # 计算垂直欧式距离
            Calculate_distance(Raw_data, start, end, Distance)

    # 计算方向误差
    avg_angle = sum(Angle) / len(Angle)
    # Angle_error=(avg_angle)/(math.pi)
    if (max(Angle) - min(Angle)) == 0:
        Angle_error = avg_angle
    else:
        Angle_error = (avg_angle - min(Angle)) / (max(Angle) - min(Angle))
    # 计算距离误差
    avg_distance = sum(Distance) / (len(Distance))
    # Distance_error=avg_distance/(1+avg_distance)
    if max(Distance) == 0:
        Distance_error = avg_distance
    else:
        Distance_error = (avg_distance - min(Distance)) / (max(Distance) - min(Distance))
    # 总的误差
    error = 1 / 2 * Angle_error + 1 / 2 * Distance_error

    return error


if __name__ == '__main__':

    # Raw_file='Raw_data.csv'
    # Feature_file='Feature_data.csv'
    # Each_error = Error_start(Raw_file, Feature_file)
    # print(Each_error)
    Raw_file = r'C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data_4.0\9'
    # Feature_file = r'C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\DPFeature_Trajectory\6'
    Feature_file = r'C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\PDFeature_Trajectory\9'
    Raw_file_list = os.listdir(Raw_file)
    Raw_file_list.sort(key=lambda fn: os.path.getatime(Raw_file + "\\" + fn))
    Feature_file_list = os.listdir(Feature_file)
    Feature_file_list.sort(key=lambda fn: os.path.getatime(Feature_file + "\\" + fn))
    N = len(Raw_file_list)
    Error = []
    for i in range(N):
        RAW_FILE_PATH = os.path.join(Raw_file, Raw_file_list[i])
        FEATURE_PATH = os.path.join(Feature_file, Feature_file_list[i])
        Each_error = Error_start(RAW_FILE_PATH, FEATURE_PATH)
        Error.append(Each_error)
        print(i)

    path1 = r'C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Error\PD9.csv'
    import pandas

    data = pandas.DataFrame({'error': Error})
    data.to_csv(path1, index=False)

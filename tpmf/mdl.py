# -*- coding:utf-8 -*-
import csv
import math
import os
from decimal import Decimal
import profile
import numpy as np


# tarjectory partition
# --------------------------------------------------------------------------------
# version 0.0

def calculate_distance(x, y):
    return np.sqrt(np.sum(np.square(x - y))) * 1000


# 计算垂直距离
def calculate_per_distance(a, b, c, d):
    ab_distance = calculate_distance(np.array(a), np.array(b))
    if ab_distance==0:
        l1=ac_distance = calculate_distance(np.array(a), np.array(c))
        l2=db_distance = calculate_distance(np.array(d), np.array(b))
    else:
        if a == c or c == b:
            l1 = 0
        else:
            ac_distance = calculate_distance(np.array(a), np.array(c))
            cb_distance = calculate_distance(np.array(c), np.array(b))
            p = (ab_distance + ac_distance + cb_distance) / 2
            S1 = math.sqrt(math.fabs(p * (p - ab_distance) * (p - ac_distance) * (p - cb_distance)))
            l1 = (2 * S1) / ab_distance
        if d == b or d == a:
            l2 = 0
        else:
            db_distance = calculate_distance(np.array(d), np.array(b))
            ad_distance = calculate_distance(np.array(a), np.array(d))
            p = (ab_distance + db_distance + ad_distance) / 2
            S2 = math.sqrt(math.fabs(p * (p - ab_distance) * (p - ad_distance) * (p - db_distance)))
            l2 = (2 * S2) / ab_distance
    if l1 == 0 and l2 == 0:
        return 0
    else:
        return (l1 * l1 + l2 * l2) / (l1 + l2)


# 计算角度距离
def calculate_angle_distance(a, b, c, d):
    ab_vec = np.array(b) - np.array(a)
    cd_vec = np.array(d) - np.array(c)
    ab_distance = np.sqrt(np.sum(np.square(ab_vec)))
    cd_distance = np.sqrt(np.sum(np.square(cd_vec)))
    if ab_distance * cd_distance == 0:
        angle_distance = 0
    else:
        cos_ = Decimal(str(np.dot(cd_vec, ab_vec))) / Decimal(str(cd_distance * ab_distance))
        if cos_>1:
            cos_=1
        elif cos_<1:
            cos_=-1
        angle = math.acos(float(cos_))
        if angle >= 0 and angle < math.pi / 2:
            angle_distance = cd_distance * 1000 * math.sin(angle)
        else:
            angle_distance = cd_distance * 1000
    return angle_distance


# 保存特征点到文件中
def Save_feature_point(point_index):
    # print(point_index)
    prim_Trajectory = open(
        r'C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data\000\Trajectory\20081203151206.plt')
    # tra_list=os.listdir(prim_Trajectory_path)
    # prim_Trajectory=os.path.join(prim_Trajectory_path, tra_list[56])
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
    feature_Trajectory = r'C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Feature_Trajectory1\0\feature_trajectory35.csv'
    feature_Trajectory_list = []
    for i in list(point_index):
        feature_Trajectory_list.append(ALL_LLT[i])
    with open(feature_Trajectory, 'w', newline='') as f:
        writer = csv.writer(f)
        for item in feature_Trajectory_list:
            writer.writerow(item)


def MDL_par(Data_list, m, n):
    x = np.array(Data_list[m][:2])
    y = np.array(Data_list[n][:2])
    xy_distance = calculate_distance(x, y)
    if xy_distance == 0:
        L_H = 0
    else:
        L_H = math.log2(xy_distance)
    perpend_distance_sum = 0
    angle_distance_sum = 0
    k=m
    while k < n:
        perpend_distance_sum = perpend_distance_sum + calculate_per_distance(Data_list[m][:2], Data_list[n][:2],
                                                                             Data_list[k][:2], Data_list[k + 1][:2])
        angle_distance_sum = angle_distance_sum + calculate_angle_distance(Data_list[m][:2], Data_list[n][:2],
                                                                           Data_list[k][:2], Data_list[k + 1][:2])
        k = k + 1
    if perpend_distance_sum == 0 or angle_distance_sum == 0:
        L_DH = 0
    else:
        L_DH = math.log2(perpend_distance_sum) + math.log2(angle_distance_sum)
    return L_H + L_DH


def MDL_nopar(Data_list, m, n):
    L_H = 0
    k=m
    while k < n:
        distance = calculate_distance(np.array(Data_list[k][:2]), np.array(Data_list[k + 1][:2]))
        if distance==0:
            L_H=0
        else:
            L_H = L_H + np.log2(distance)
        k= k + 1
    return L_H


# 读取数据并转换类型
def readData(trajectory):
    file = os.path.join(trajectory_path, trajectory)
    Data_list = []
    # 读取数据文件，并保存到Data_list
    with open(file, 'r') as f:
        data_list = csv.reader(f)
        for row in data_list:
            Data_list.append(row)

    # print(Data_list)
    # Data_list将集合里的字符串类型转换成数值类型
    for point in Data_list:
        point[0] = float(point[0])
        point[1] = float(point[1])
    return Data_list


# 轨迹划分
def trajectory_partition(Data_list):
    Feature_point = []  # 特征点集合
    # Data_list_copy = copy.copy(Data_list)
    # 将第一个点加入到特征集合中
    Feature_point.append(Data_list[0])
    start_index = 0
    length = 1
    import time
    start=time.clock()
    while (start_index + length < len(Data_list)):
        current_index = start_index + length
        cost_par = MDL_par(Data_list, start_index, current_index)
        cost_nopar = MDL_nopar(Data_list, start_index, current_index)
        if cost_par > cost_nopar:
            Feature_point.append(Data_list[current_index-1])
            start_index = current_index-1
            length = 1
        else:
            length = length + 1
    Feature_point.append(Data_list[len(Data_list) - 1])
    end=time.clock()
    print(end-start)
    print(len(Feature_point))
    # 保存特征点对应的索引
    # points_index = []
    # for item in Feature_point:
    #     if item in Data_list_copy:
    #         points_index.append(Data_list_copy.index(item))
    # Save_feature_point(points_index)
    return Feature_point


# -------------------------------------------------------------------------------
if __name__ == '__main__':
    trajectory_path = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data_4.0\0"
    trajectory_list = os.listdir(trajectory_path)
    # 按时间顺序读取文件
    trajectory_list.sort(key=lambda fn: os.path.getatime(trajectory_path + "\\" + fn))
    # print(trajectory_list)
    Data_list = []
    Feaure_list = []
    for i in range(len(trajectory_list)):
        Data_list.append(readData(trajectory_list[i]))
    # start=time.clock()
    # for j in range(len(Data_list)):
    #     Feaure_list.append(trajectory_partition(Data_list[j]))
    partition_result = trajectory_partition(Data_list[0])
    # end=time.clock()
    # print(end-start)
    # 写入到csv文件
    with open('Raw_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for item in Data_list[0]:
            writer.writerow(item)
    with open('Feature_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in partition_result:
            writer.writerow(row)

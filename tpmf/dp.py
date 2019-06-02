# -*- coding:utf-8 -*-
import csv
import math
import os
import profile
import numpy as np


# import matplotlib.pyplot as plot


# tarjectory partition
# --------------------------------------------------------------------------------
# version 1.0
#两个点之间的距离
def calculate_distance(x, y):
    return np.sqrt(np.sum(np.square(x - y))) * math.pow(10, 3)


#点到线段的距离
def vertical_distance(A, B ,x):
    AB_distance = calculate_distance(np.array(A), np.array(B))
    Ax_distance = calculate_distance(np.array(A), np.array(x))
    Bx_distance = calculate_distance(np.array(B), np.array(x))
    if AB_distance==0:
        return Ax_distance
    elif Ax_distance==0 or Bx_distance==0:
        return 0
    else:
        p=(AB_distance+Ax_distance+Bx_distance)/2
        S=math.sqrt(math.fabs(p*(p-AB_distance)*(p-Ax_distance)*(p-Bx_distance)))
        return (2*S)/AB_distance

#DP algorithm
def DP_compress(Data_list, Feature_point, max_value):
    start_index=0
    end_index=len(Data_list)-1
    if start_index<end_index:
        index=start_index+1
        max_vertical_distance=0
        key_point_index=0
        while index<end_index:
            curr_distance=vertical_distance(Data_list[start_index][:2], Data_list[end_index][:2], Data_list[index][:2])
            if curr_distance>=max_vertical_distance:
                max_vertical_distance=curr_distance
                key_point_index=index
            index=index+1
        if max_vertical_distance>=max_value:
            Feature_point.append(Data_list[key_point_index])
            DP_compress(Data_list[start_index:key_point_index+1], Feature_point, max_value)
            DP_compress(Data_list[key_point_index:end_index+1], Feature_point, max_value)


#去除冗余的数据
def RemoveDuplicates(Feature_point):
    l2 = []
    [l2.append(i) for i in Feature_point if not i in l2]
    return l2


#保存特征点到文件中
def Save_feature_point(point_index):
    # print(point_index)
    prim_Trajectory= open(r'C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data\000\Trajectory\20081023025304.txt')
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
    feature_Trajectory = r'C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Feature_Trajectory2\0\feature_trajectory1.csv'
    feature_Trajectory_list = []
    for i in list(point_index):
        # print(i)
        feature_Trajectory_list.append(ALL_LLT[i])
    with open(feature_Trajectory, 'w', newline='') as f:
        writer = csv.writer(f)
        for item in feature_Trajectory_list:
            writer.writerow(item)


#读取数据并转换类型
def readData(trajectory):
    file = os.path.join(trajectory_path, trajectory)
    # Feature_point = []  # 特征点集合
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


#轨迹划分
def trajectory_partition(Data_list):
    Feature_point=[]
    Feature_point.append(Data_list[0])
    Feature_point.append(Data_list[len(Data_list)-1])
    import time
    start=time.clock()
    DP_compress(Data_list, Feature_point, 6)
    end=time.clock()
    Feature_points=sorted(Feature_point, key=lambda x:x[2])
    #保存特征点对应的索引
    # points_index = []
    # for item in Feature_points:
    #     if item in Data_list_copy:
    #         points_index.append(Data_list_copy.index(item))
    # Save_feature_point(points_index)
    return Feature_points,end-start


# -------------------------------------------------------------------------------
if __name__ == '__main__':
    trajectory_path = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data_4.0\9"
    trajectory_list = os.listdir(trajectory_path)
    # 按时间顺序读取文件
    trajectory_list.sort(key=lambda fn: os.path.getatime(trajectory_path + "\\" + fn))
    path2 = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\DPFeature_Trajectory\9"
    Data_list = []#存储一个用户的所有轨迹数据
    Time=[]
    Number=[]
    for i in range(len(trajectory_list)):
        Data_list.append(readData(trajectory_list[i]))
    for j in range(len(Data_list)):
        Feature_data, time = trajectory_partition(Data_list[j])
        Time.append(time)
        Number.append(len(Feature_data))
        fileName = "Trajectory" + str(j + 1) + ".csv"
        filePath2 = os.path.join(path2, fileName)
        with open(filePath2, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in Feature_data:
                writer.writerow(row)

    path3 = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Time\DPtime9.csv"
    path4 = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\NumberPoints\DP9.csv"
    import pandas as pd

    dataframe1 = pd.DataFrame({'time': Time})
    dataframe1.to_csv(path3, index=False)

    dataframe2 = pd.DataFrame({'Number': Number})
    dataframe2.to_csv(path4, index=False)
    # FP=trajectory_partition(Data_list[0])
    # print(len(FP))
    # #写入到csv文件
    # with open('Raw_data.csv', 'w', newline='') as f:
    #     writer=csv.writer(f)
    #     for item in Data_list[0]:
    #         writer.writerow(item)
    # with open('Feature_data.csv', 'w', newline='') as f:
    #     writer=csv.writer(f)
    #     for item in FP:
    #         writer.writerow(item)
    # print(end - start)
    # partition_result = trajectory_partition(trajectory_list[0])


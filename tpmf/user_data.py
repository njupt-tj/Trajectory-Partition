# -*-coding:utf-8-*-
# Read user's datasets
#convert latitude and longtude into XY coordinate
import os
import math
import csv

# filename = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data\000\Trajectory\20081026134407.plt"
# user1_data=[]
# lat_data=[]
# long_data=[]
# with open(filename) as f:
#     lines=f.readlines()
#     for line in lines:
#         user1_data.append(tuple(line.split(','))[:2])
#         # lat.append((line[:9]))
#
# # ------------------------------------------------------------------------------------
# print(user1_data)
#
# for item in user1_data:
#     lat_data.append(float(item[0]))
#     long_data.append(float(item[1]))
#
# print(lat_data)
# print(long_data)
#
# #---------------------------------------------------------------------------------
# #画轨迹图
# import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
# plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# plt.figure(figsize=(10,10))
# plt.plot(lat_data,long_data,'b-',linewidth=1.0)
# plt.grid()
# plt.xlim(39.00,41.00)
# plt.ylim(115.00,118.00)
# plt.show()



# ---------------------------------------------------------------------------------
# Read all data of user during all the days

# user_data=[]
# lat_data=[]
# long_data=[]
# time_data=[]
# user_data_dir=r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data\006\Trajectory"
# user_data_list=os.listdir(user_data_dir)
# # print(user_data_list)
# for every_data in user_data_list:
#     read_every_data=open(os.path.join(user_data_dir, every_data))
#     for line in read_every_data.readlines():
#         # if '31.167747' in line:
#         #     print(read_every_data)
#         if line.__len__()>50:
#             user_data.append(tuple(line.split(','))[:2])
#             time_data.append(line.split(',')[-1])
#
#
#
#  print(user_data)
#
# for item in user_data:
#     lat_data.append(float(item[0]))
#     long_data.append(float(item[1]))
#
# print(lat_data.__len__())
# print(long_data.__len__())
# print(min(lat_data),end=' ')
# print(max(lat_data))
# print(min(long_data),end=' ')
# print(max(long_data))
#--------------------------------------------------------------------------------------
#version 1.0
#读取数据集
LLT_data=[]
every_LLT_data=[]
all_LLT_data=[]
user_data_dir=r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data\009\Trajectory"
user_data_list=os.listdir(user_data_dir)
# print(user_data_list)
for every_data in user_data_list:
    read_every_data=open(os.path.join(user_data_dir, every_data))
    for line in read_every_data.readlines():
        if line.__len__()>50:
            LLT_data.append(float(line.split(',')[0]))
            LLT_data.append(float(line.split(',')[1]))
            LLT_data.append(line.split(',')[-1].strip())
            every_LLT_data.append(LLT_data)
            LLT_data=[]
            # user_data.append(tuple(line.split(','))[:2])
            # time_data.append(line.split(',')[-1].strip())
    all_LLT_data.append(every_LLT_data)
    every_LLT_data=[]

sum=0
for i in range(len(all_LLT_data)):
    sum=sum+len(all_LLT_data[i])
print(sum)
#--------------------------------------------------------------------------------------
# 将经纬度转化为xy坐标
path=r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data_4.0"

new_data_list=os.listdir(path)
print(new_data_list)
def LL_TO_XY(all_LLT_data, path):
    TO_XY_coordinate=[]
    temp_XY=[]
    xy=[]
    for i in range(len(all_LLT_data)):
        for j in all_LLT_data[i]:
            temp_XY.append(float((j[1]-116.399865)*111*math.cos(j[0]*math.pi/180)))
            temp_XY.append(float((j[0]-39.910521)*111))
            temp_XY.append(j[2])
            xy.append(temp_XY)
            temp_XY=[]
        TO_XY_coordinate.append(xy)
        xy=[]

    # print(TO_XY_coordinate)

# 将转换后的xy坐标存储到csv文件
    STORGE_file='Trajectory'
    os.mkdir(os.path.join(path, str(10)))
    for i in range(len(TO_XY_coordinate)):
        file_name=STORGE_file+str(i)+'.csv'
        file_path=os.path.join(os.path.join(path, str(10)), file_name)
        # file_path = os.path.join(parent_file, file_name)
        with open(file_path, 'w', newline='') as data_xy_file:
            writer=csv.writer(data_xy_file)
            for current_list in TO_XY_coordinate[i]:
                writer.writerow(current_list)


LL_TO_XY(all_LLT_data, path)
#-----------------------------------------------------------------------------------
#version 2.0
#读取数据集
# def read_data(user_data_dir, user_data_list):
#     LLT_data=[]
#     every_LLT_data=[]
#     all_LLT_data=[]
#     for every_data in user_data_list:
#         read_every_data=open(os.path.join(user_data_dir, every_data))
#         for line in read_every_data.readlines():
#             if line.__len__()>50:
#                 LLT_data.append(float(line.split(',')[0]))
#                 LLT_data.append(float(line.split(',')[1]))
#                 LLT_data.append(line.split(',')[-1].strip())
#                 every_LLT_data.append(LLT_data)
#                 LLT_data=[]
#                 # user_data.append(tuple(line.split(','))[:2])
#                 # time_data.append(line.split(',')[-1].strip())
#         all_LLT_data.append(every_LLT_data)
#         every_LLT_data=[]
#     return all_LLT_data
#
#
# print(all_LLT_data)
#--------------------------------------------------------------------------------------
# 将经纬度转化为xy坐标
# new_data_list=os.listdir(path)
# print(new_data_list)
# def LL_TO_XY(all_LLT_data, path, user_id):
#     TO_XY_coordinate=[]
#     temp_XY=[]
#     xy=[]
#     for i in range(len(all_LLT_data)):
#         for j in all_LLT_data[i]:
#             temp_XY.append(float((j[1]-116.399865)*111*math.cos(j[0])))
#             temp_XY.append(float((j[0]-39.910521)*111))
#             temp_XY.append(j[2])
#             xy.append(temp_XY)
#             temp_XY=[]
#         TO_XY_coordinate.append(xy)
#         xy=[]

    # print((TO_XY_coordinate))
#将转换后的xy坐标存储到csv文件
    # STORGE_file='Trajectory'
    # os.mkdir(os.path.join(path, user_id))
    # for i in range(len(TO_XY_coordinate)):
    #     # str1=str(i)
    #     file_name=STORGE_file+repr(i)+'.csv'
    #     file_path=os.path.join(os.path.join(path, user_id), file_name)
    #     # file_path = os.path.join(parent_file, file_name)
    #     with open(file_path, 'w', newline='') as data_xy_file:
    #         writer=csv.writer(data_xy_file)
    #         for current_list in TO_XY_coordinate[i]:
    #             writer.writerow(current_list)

# ----------------------------------------------------------------------------------------
# 循环控制读取数据集并且处理数据最后保存文件
# if __name__ == '__main__':
    # user_data_filedir=r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data"
    # path=r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data_3.0"
    # user_data_listfile=os.listdir(user_data_filedir)
    # user_id=[]
    # for i in range(182):
    #     user_id.append(str(i))
    # k=0
    # for current_listfile in user_data_listfile:
    #     str='Trajectory'
    #     current_tra_path=os.path.join(os.path.join(user_data_filedir, current_listfile), str)
    #     user_data_list1 = os.listdir(current_tra_path)
    #     read_user_data=read_data(current_tra_path, user_data_list1)
    #     LL_TO_XY(read_user_data, path, user_id[k])
    #     k=k+1
#---------------------------------------------------------------------------------------







# -*-coding:utf-8-*-
# Read user's datasets
# convert latitude and longtude into XY coordinate
import csv
import math
import os

# 读取数据集

# --------------------------------------------------------------------------------------
def transform_and_save(all_data, path):
    xy_coordinates = []
    temp_xy = []
    xy = []
    for i in range(len(all_data)):
        for j in all_data[i]:
            temp_xy.append(float((j[1] - 116.399865) * 111 * math.cos(j[0] * math.pi / 180)))
            temp_xy.append(float((j[0] - 39.910521) * 111))
            temp_xy.append(j[2])
            xy.append(temp_xy)
            temp_xy = []
        xy_coordinates.append(xy)
        xy = []

    # 将转换后的xy坐标存储到csv文件
    save_filename = 'Trajectory'
    os.mkdir(os.path.join(path, str(10)))
    for i in range(len(xy_coordinates)):
        file_name = save_filename + str(i) + '.csv'
        file_path = os.path.join(os.path.join(path, str(10)), file_name)
        with open(file_path, 'w', newline='') as data_xy_file:
            writer = csv.writer(data_xy_file)
            for current_list in xy_coordinates[i]:
                writer.writerow(current_list)


if __name__ == '__main__':
    data = []
    each_file_data = []
    all_data = []
    traj_data_dir = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data\001\Trajectory"
    path = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data_4.0"
    data_list = os.listdir(traj_data_dir)
    for every_file in data_list:
        read_every_data = open(os.path.join(traj_data_dir, every_file))
        for line in read_every_data.readlines():
            if line.__len__() > 50:
                data.append(float(line.split(',')[0]))
                data.append(float(line.split(',')[1]))
                data.append(line.split(',')[-1].strip())
                each_file_data.append(data)
                data = []
        all_data.append(each_file_data)
        each_file_data = []
    # 转换
    transform_and_save(all_data, path)

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
# ---------------------------------------------------------------------------------------

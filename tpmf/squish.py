# -*- coding:utf-8 -*-
from queue import PriorityQueue
from queue import Queue
import math
import os
import csv


# 利用优先队列
# 该算法要求一个输入参数buffer(缓冲区大小)
# 初始化所有进来的GPS点都进入缓冲区，直到缓冲区满
# 一旦缓冲区满了，任何一个新进来的GPS点都要要求缓冲区删除一个点
# 目标就是要移除那些包含信息最少的点

# 定义一个点类
class Point:
    """
    id:GPS点的唯一编号
    x:横坐标
    y:纵坐标
    t:时间戳
    """

    def __init__(self, id, x, y, t):
        self.__id = id
        self.__x = x
        self.__y = y
        self.__t = t

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_t(self, t):
        self.__t = t

    def get_x(self):
        return self.__x;

    def get_y(self):
        return self.__y

    def get_t(self):
        return self.__t


class PointWithSED:
    """
    id:一个GPS点的唯一编号
    sed:同步时间距离
    """

    def __init__(self, id, sed):
        self.__id = id
        self.__sed = sed

    def set_sed(self, new_sed):
        self.__sed = new_sed

    def get_id(self):
        return self.__id

    def get_sed(self):
        return self.__sed

    def __lt__(self, other):
        return self.__sed < other.get_sed()


def time_diff(t1, t2):
    s1 = '%s %s' % ('2019-6-3', t1)
    s2 = '%s %s' % ('2019-6-3', t2)
    # 字符串转时间格式
    d1 = datetime.datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(s2, '%Y-%m-%d %H:%M:%S')
    return (d2 - d1).total_seconds()


# 计算sed(时间同步距离)
def calculate_sed(left_point, middle_point, right_point):
    ml_time_diff = time_diff(left_point.get_t(), middle_point.get_t())
    ls_time_diff = time_diff(left_point.get_t(), right_point.get_t())
    if ls_time_diff == 0:
        time_ratio = 1
    else:
        time_ratio = ml_time_diff / ls_time_diff
    new_x = left_point.get_x() + (right_point.get_x() - left_point.get_x()) * time_ratio
    new_y = left_point.get_y() + (right_point.get_y() - left_point.get_y()) * time_ratio
    x_diff = middle_point.get_x() - new_x
    y_diff = middle_point.get_y() - new_y
    return math.sqrt(x_diff * x_diff + y_diff * y_diff)


# points:GPS点的个数
# commpression_ratio:压缩率
def squish(points, compression_ratio):
    size = len(points)
    buffer_size = (int)(size * compression_ratio)  # 缓冲区大小
    buffer_sed = PriorityQueue()
    compressed_points = []
    compressed_points.append(points[0])
    firstSED = PointWithSED(0, float('inf'))
    buffer_sed.put(firstSED)
    if buffer_size > 2:
        compressed_points.append(points[1])
        for i in range(2, size):
            # 计算前面一个点的sed
            previous_sed = calculate_sed(points[i], points[i - 1], points[i - 2])
            point_with_sed = PointWithSED(i - 1, previous_sed)
            buffer_sed.put(point_with_sed)
            # 缓冲区已经满了，从缓冲区删除一个sed最小的点
            if (len(compressed_points) >= buffer_size):
                least_point = buffer_sed.get()
                acquire_id = least_point.get_id()
                acquire_sed = least_point.get_sed()
                # 从缓冲区中删除sed最小的点
                compressed_points.remove(points[acquire_id])
                left_id = acquire_id - 1
                right_id = acquire_id + 1
                queue = Queue()
                left_flag = False
                right_flag = False
                while buffer_sed.qsize() > 0:
                    temp_point = buffer_sed.get()
                    temp_id = temp_point.get_id()
                    temp_sed = temp_point.get_sed()
                    if (temp_id != 0 and temp_id == left_id):
                        temp_point.set_sed(temp_sed + acquire_sed)
                        left_flag = True
                    if (temp_id == right_id):
                        temp_point.set_sed(temp_sed + acquire_sed)
                        right_flag = True
                    queue.put(temp_point)
                    if (left_flag and right_flag):
                        break
                while queue.qsize() != 0:
                    buffer_sed.put(queue.get())
            compressed_points.append(points[i])
    return compressed_points


def read_data(file):
    #具体路径
    file_path=os.path.join(path,file)
    data=[]
    with open(file_path,'r') as f:
        lines=csv.reader(f)
        for line in lines:
            data.append(line)
    for point in data:
        point[0]=float(data[0])
        point[1]=float(data[1])
    return data


if __name__ == '__main__':
    # 读取轨迹数据
    tradata = []
    points=[]#数据流
    #文件目录路径
    path = r"C:\Users\TJ\Desktop\Dataset\Geolifep Trajectories 1.3\Data_4.0\0"
    file_list=os.listdir(path)
    file_list.sort(key=lambda fn: os.path.getatime(trajectoryPath + "\\" + fn))
    #读取每个文件的轨迹数据
    for i in range(len(file_list)):
        tradata.append(read_data(file_list[i]))
    id=0
    for j in range(len(tradata)):
        for point in tradata[j]:
            p=Point(id,point[0],point[1],point[2])
            points.append(p)
            id=id+1
        #测试轨迹的个数
        if j==0:
            break
    #传入参数：points:数据  0.25:压缩率
    result=squish(points,0.25)
    for point in result:
        print(point.get_id())


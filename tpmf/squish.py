# -*- coding:utf-8 -*-
import os
import time
from queue import PriorityQueue
from queue import Queue

import distances
from point import Point
from read_data import read
import write_data


# 利用优先队列
# 该算法要求一个输入参数buffer(缓冲区大小)
# 初始化所有进来的GPS点都进入缓冲区，直到缓冲区满
# 一旦缓冲区满了，任何一个新进来的GPS点都要要求缓冲区删除一个点
# 目标就是要移除那些包含信息最少的点


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


def find_min_index(buffer_sed):
    min_sed = float('inf')
    k = 0
    for i in range(len(buffer_sed)):
        point_with_sed = buffer_sed[i]
        if point_with_sed.get_sed() < min_sed:
            min_sed = point_with_sed.get_sed()
            k = i
    min_index = buffer_sed[k].get_id()
    buffer_sed.remove(buffer_sed[k])
    return min_index, min_sed


def update(buffer_sed, left_id, right_id, min_sed):
    flag_left = False
    flag_right = False
    for point_with_sed in buffer_sed:
        cur_id = point_with_sed.get_id()
        cur_sed = point_with_sed.get_sed()
        if cur_id == left_id:
            point_with_sed.set_sed(min_sed + cur_sed)
            flag_left = True
        if cur_id == right_id:
            point_with_sed.set_sed(min_sed + cur_sed)
            flag_right = True
        if flag_left and flag_right:
            break


# points:GPS点的个数
# commpression_ratio:压缩率
def squish(compression_ratio):
    size = len(points)
    buffer_size = int(size / compression_ratio)  # 缓冲区大小
    # buffer_sed = PriorityQueue()
    buffer_sed = []
    compressed_points = []
    compressed_points.append(points[0])
    firstSED = PointWithSED(0, float('inf'))
    buffer_sed.append(firstSED)
    if buffer_size > 2:
        compressed_points.append(points[1])
        for i in range(2, size):
            # 计算前面一个点的sed
            previous_sed = distances.sed_distance(points[i], points[i - 1], points[i - 2])
            point_with_sed = PointWithSED(i - 1, previous_sed)
            buffer_sed.append(point_with_sed)
            # 缓冲区已经满了，从缓冲区删除一个sed最小的点
            if len(compressed_points) >= buffer_size:
                min_index, min_sed = find_min_index(buffer_sed)
                compressed_points.remove(points[min_index])
                left_id = min_index - 1
                right_id = min_index + 1
                update(buffer_sed, left_id, right_id, min_sed)
            compressed_points.append(points[i])
    return compressed_points


if __name__ == '__main__':
    # 读取轨迹数据
    tradata = []
    # 文件目录路径
    raw_path = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data_4.0\2"
    new_path = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\SQUISH\squish_data\9"
    file_list = os.listdir(raw_path)
    file_list.sort(key=lambda x: x[10:-5])
    # 读取每个文件的轨迹数据
    for i in range(len(file_list)):
        tradata.append(read(raw_path, file_list[i]))
    time_records = []
    compression_ratios = []
    compression_ratio = 5
    total_time = 0
    for j in range(len(tradata)):
        id = 0
        points = []
        for point in tradata[j]:
            p = Point(id, point[0], point[1], point[2])
            points.append(p)
            id = id + 1
        # 传入参数：5:压缩比
        start_time = time.clock()
        result = squish(compression_ratio)
        end_time = time.clock()
        time_records.append(end_time - start_time)
        total_time += end_time - start_time
        cmp_ratio = (1 - len(result) / len(points)) * 100
        compression_ratios.append(cmp_ratio)
        #write_data.write(result, new_path, j)

    print(total_time)
    timepath = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\SQUISH\time\2.csv"
    # = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\SQUISH\cmp_ratio\9.csv"
    write_data.write_time(time_records, timepath)
    #write_data.write_compressionRatio(compression_ratios, compressRatio_path)

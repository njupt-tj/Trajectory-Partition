# -*- coding:utf-8 -*-
import os
import time
from queue import PriorityQueue
from queue import Queue

import distances
from point import Point
from read_data import read


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


# points:GPS点的个数
# commpression_ratio:压缩率
def squish(compression_ratio):
    size = len(points)
    buffer_size = int(size / compression_ratio)  # 缓冲区大小
    buffer_sed = PriorityQueue()
    compressed_points = []
    compressed_points.append(points[0])
    firstSED = PointWithSED(0, float('inf'))
    buffer_sed.put(firstSED)
    if buffer_size > 2:
        compressed_points.append(points[1])
        for i in range(2, size):
            # 计算前面一个点的sed
            previous_sed = distances.sed_distance(points[i], points[i - 1], points[i - 2])
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


if __name__ == '__main__':
    # 读取轨迹数据
    tradata = []
    # 文件目录路径
    raw_path = r"F:\dataset\rawData\0"
    new_path = r"F:\dataset\squishData\0"
    file_list = os.listdir(raw_path)
    file_list.sort(key=lambda x: x[10:-5])
    # 读取每个文件的轨迹数据
    for i in range(len(file_list)):
        tradata.append(read(raw_path, file_list[i]))
    time_records = []
    compression_ratios = []
    compression_ratio=5
    total_time=0
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
        total_time+=end_time-start_time
        cmp_ratio = (1 - len(result) / len(points)) * 100
        compression_ratios.append(cmp_ratio)
        #write_data.write(result, new_path, j)
        print(j)

    print(total_time)
    # timepath = r"F:\dataset\squishData\time0.csv"
    # compressRatio_path = r"F:\dataset\squishData\numbers0.csv"
    # write_data.write_time(time_records, compressRatio_path)
    # write_data.write_compressionRatio(compression_ratios, compressRatio_path)

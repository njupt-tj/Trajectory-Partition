# -*- coding:utf-8 -*-
import numpy as np
import os
import time
import distances
import write_data
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
    pi：邻居的sed，如果左右邻居没有被移除，则pi默认为0
    """

    def __init__(self, id, sed, pi):
        self.__id = id
        self.__sed = sed
        self.__pi = pi

    def set_sed(self, new_sed):
        self.__sed = new_sed

    def set_pi(self, new_pi):
        self.__pi = new_pi

    def get_id(self):
        return self.__id

    def get_sed(self):
        return self.__sed

    def get_pi(self):
        return self.__pi

    def __lt__(self, other):
        return self.__sed < other.get_sed()


# 更新邻居节点的pi值
def update(min_index, min_priority):
    buffer_sed[min_index - 1].set_pi(np.maximum(min_priority, buffer_sed[min_index - 1].get_pi()))
    if min_index+1>=len(buffer_sed):
        print("超出范围")
    buffer_sed[min_index + 1].set_pi(np.maximum(min_priority, buffer_sed[min_index + 1].get_pi()))
    if min_index - 2 >= 0:
        adjust_priority(min_index-2, min_index-1, min_index+1)
    if min_index + 2 < len(buffer_sed):
        adjust_priority(min_index-1, min_index+1, min_index+2)
    # 删除优先级最小的点
    buffer_sed.remove(buffer_sed[min_index])


# 找到优先级最低的点，并返回点的编号
def find_mini_priority():
    min_sed = buffer_sed[0].get_sed()
    min_index = 0
    for i in range(1, len(buffer_sed)):
        if (buffer_sed[i].get_sed() < min_sed):
            min_sed = buffer_sed[i].get_sed()
            min_index = i
    return min_index


# 调整优先级
def adjust_priority(cur_index, pre_index, ppre_index):
    if pre_index < 0 or ppre_index < 0:
        return
    pre_id = buffer_sed[pre_index].get_id()
    ppre_id = buffer_sed[ppre_index].get_id()
    cur_id = buffer_sed[cur_index].get_id()
    sed_error = buffer_sed[pre_index].get_pi() + distances.sed_distance(points[ppre_id], points[pre_id], points[cur_id])
    buffer_sed[pre_index].set_sed(sed_error)


# points:GPS点的个数
# commpression_ratio:压缩率
def squish(cmp_ratio, sed_error):
    size = len(points)
    capacity = int(size / cmp_ratio)  # 缓冲区大小
    i = 0
    if capacity>2:
        while i < size:
            if (i / cmp_ratio) >= capacity:
                capacity += 1
            # 新来的点设为sed_error设为无穷大
            buffer_sed.append(PointWithSED(i, float('inf'), 0))
            # pi不是第一个点
            if i > 0:
                buffer_size = len(buffer_sed)
                adjust_priority(buffer_size - 1, buffer_size - 2, buffer_size - 3)
            # 此时，缓冲区满了
            if len(buffer_sed) == capacity:
                # 找到具有最小的优先级的点
                min_index = find_mini_priority()
                min_priority = buffer_sed[min_index].get_sed()
                # 更新
                update(min_index, min_priority)
            i += 1
        min_index = find_mini_priority()
        min_priority = buffer_sed[min_index].get_sed()
        # 未达到sed_error重复移除最小优先权的点
        while (min_priority <= sed_error):
            update(min_index, min_priority)
            min_index = find_mini_priority()
            min_priority = buffer_sed[min_index].get_sed()
    else:
        buffer_sed.append(PointWithSED(0,float('inf'),0))
        buffer_sed.append(PointWithSED(size-1,float('inf'),0))


def get_pid(buffer_sed):
    pids=[]
    for pointwithSED in buffer_sed:
        pids.append(pointwithSED.get_id())
    return pids

if __name__ == '__main__':
    # 读取轨迹数据
    tradata = []
    # 文件目录路径
    raw_path = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Data_4.0\9"
    new_path = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\SQUISH-E\squish_e_data\3"
    file_list = os.listdir(raw_path)
    file_list.sort(key=lambda x: x[10:-5])
    # 读取每个文件的轨迹数据
    for i in range(len(file_list)):
        tradata.append(read(raw_path, file_list[i]))
    time_records = []
    compression_ratios = []
    error_bound = 10
    compression_ratio=5
    total_time = 0
    for j in range(len(tradata)):
        id = 0
        points = []
        for point in tradata[j]:
            p = Point(id, point[0], point[1], point[2])
            points.append(p)
            id = id + 1
        buffer_sed = []
        start_time = time.clock()
        squish(compression_ratio, error_bound)
        end_time = time.clock()
        time_records.append(end_time - start_time)
        total_time += end_time - start_time
        cmp_ratio = (1 - len(buffer_sed) / len(points)) * 100
        compression_ratios.append(cmp_ratio)
        compressed_pointsId=get_pid(buffer_sed)
        #write_data.write1(points, compressed_pointsId, new_path, j)

    print(total_time)
    timepath = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\SQUISH-E\time\9.csv"
    #compressRatio_path = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\SQUISH-E\cmp_ratio\9.csv"
    write_data.write_time(time_records, timepath)
    #write_data.write_compressionRatio(compression_ratios, compressRatio_path)

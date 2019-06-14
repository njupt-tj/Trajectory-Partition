# -*- coding:utf-8 -*-
import math
import os
import time

import distances
import write_data
from point import Point

'''
One-Pass Error Bounded Trajectory Simplificatin
'''


# 线段类
class LineSegment:
    def __init__(self, start_p, end_p):
        self.__start_p = start_p
        self.__end_p = end_p

    def get_start(self):
        return self.__start_p

    def get_end(self):
        return self.__end_p

    def get_distance(self):
        return distances.point_distance(self.__start_p, self.__end_p)


class PointWithoutId:
    def __init__(self, x_coordinate, y_coordinate):
        self.__x = x_coordinate
        self.__y = y_coordinate

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y


# start_point:开始点
# cur_active_point:当前活跃的点
# cur_line_segment:当前有向线段
def get_active_point(start_point, cur_active_point, cur_line_segment, error_bound):
    s = start_point.get_id()
    a = cur_active_point.get_id()
    i = a + 1
    flag = True
    if i < len(points):
        R_i = LineSegment(start_point, points[i])
        while (R_i.get_distance() - cur_line_segment.get_distance()) <= error_bound / 4 and i < len(points) and (
                i - s) < 4 * math.pow(10, 5):
            dis_i_la = distances.perpendicular_distance(cur_line_segment.get_start(), points[i],
                                                        cur_line_segment.get_end())
            R_a = LineSegment(start_point, cur_active_point)
            dis_i_ra = distances.perpendicular_distance(R_a.get_start(), points[i], R_a.get_end())
            if dis_i_la > error_bound / 2 or dis_i_ra > error_bound:
                flag = False
                break;
            i += 1
            if i >= len(points):
                break
            R_i = LineSegment(start_point, points[i])
        if i < len(points):
            dis_i_la = distances.perpendicular_distance(cur_line_segment.get_start(), points[i],
                                                        cur_line_segment.get_end())
            if dis_i_la > error_bound / 2 and cur_line_segment.get_distance() > 0:
                flag = False
    if i == len(points):
        i = -1
    return i, flag


# 计算角度
def calc_angle(line_segment):
    start_p = line_segment.get_start()
    end_p = line_segment.get_end()
    x_diff = end_p.get_x() - start_p.get_x()
    y_diff = end_p.get_y() - start_p.get_y()
    sqre = math.sqrt(x_diff * x_diff + y_diff * y_diff)
    if x_diff <= 0 and y_diff < 0:
        angle = math.pi + math.acos(-x_diff / sqre)
    elif x_diff > 0 and y_diff < 0:
        angle = 3 / 2 * math.pi + math.acos(x_diff / sqre)
    else:
        angle = math.acos(x_diff / sqre)
    return angle


# 计算终点
def calc_endp(length, angle, s):
    start_p = points[s]
    x_diff = length * math.cos(angle)
    y_diff = length * math.sin(angle)
    new_x = start_p.get_x() + x_diff
    new_y = start_p.get_y() + y_diff
    end_p = PointWithoutId(new_x, new_y)
    return end_p


def assign(R_i, cur_line_segment):
    R_angle = calc_angle(R_i)
    l_angle = calc_angle(cur_line_segment)
    angle_diff = R_angle - l_angle
    if (angle_diff > -2 * math.pi and angle_diff <= -3 / 2 * math.pi) or (
            angle_diff >= -math.pi and angle_diff <= -1 / 2 * math.pi
    ) or (angle_diff >= 0 and angle_diff <= 1 / 2 * math.pi) or (
            angle_diff >= math.pi and angle_diff <= 3 / 2 * math.pi):
        f = 1
    else:
        f = -1
    return f


def fit_function(s, cur_active_point, cur_line_segment, error_bound):
    a = cur_active_point.get_id()
    R_i = LineSegment(points[s], points[a])
    next_line_segment = None
    # 活跃点所处区域
    j = math.ceil(R_i.get_distance() * (2 / error_bound) - 0.5)
    if R_i.get_distance() - cur_line_segment.get_distance() <= error_bound / 4:
        next_line_segment = cur_line_segment
    elif R_i.get_distance() > error_bound / 4 and cur_line_segment.get_distance() == 0:
        length = (j * error_bound / 2) / 1000
        angle = calc_angle(R_i)
        end_point = calc_endp(length, angle, s)
        next_line_segment = LineSegment(points[s], end_point)
    else:
        length = (j * error_bound / 2) / 1000
        dis = distances.perpendicular_distance(cur_line_segment.get_start(), points[a], cur_line_segment.get_end())
        div = dis / (j * error_bound / 2)
        if div > 1:
            div = 1
        angle = calc_angle(cur_line_segment) + assign(R_i, cur_line_segment) * math.asin(div) / j
        end_point = calc_endp(length, angle, s)
        next_line_segment = LineSegment(points[s], end_point)
    return next_line_segment


def operb(error_bound):
    # 初始化
    s = 0
    a = 0
    e = s;
    cur_line_segment = LineSegment(points[s], points[e])
    a, flag = get_active_point(points[s], points[a], cur_line_segment, error_bound)
    while a != -1 and points[a] != None:
        s = e
        cur_line_segment = LineSegment(points[s], points[s])
        cur_line_segment = fit_function(s, points[a], cur_line_segment, error_bound)
        a, flag = get_active_point(points[s], points[a], cur_line_segment, error_bound)
        while a != -1 and points[a] != None and flag == True:
            cur_line_segment = fit_function(s, points[a], cur_line_segment, error_bound)
            e = a
            a, flag = get_active_point(points[s], points[a], cur_line_segment, error_bound)
        compressed_points.append([s, e])


def process(compressed_points):
    noduplicate_points = []
    for presention in compressed_points:
        if presention[0] == presention[1]:
            continue
        noduplicate_points.append(presention[0])
    noduplicate_points.append(compressed_points[-1][1])
    return noduplicate_points


if __name__ == '__main__':
    # 读取轨迹数据
    tradata = []
    # 文件目录路径
    raw_path = r"F:\dataset\rawData\0"
    new_path = r"F:\dataset\operbData\0"
    file_list = os.listdir(raw_path)
    file_list.sort(key=lambda x: x[10:-5])
    # 读取每个文件的轨迹数据
    for i in range(len(file_list)):
        tradata.append(read(raw_path, file_list[i]))
    time_records = []
    compression_ratios = []
    error_bound = 6
    total_time = 0
    for j in range(len(tradata)):
        id = 0
        points = []
        for point in tradata[j]:
            p = Point(id, point[0], point[1], point[2])
            points.append(p)
            id = id + 1
        compressed_points = []
        start_time = time.clock()
        operb(error_bound)
        end_time = time.clock()
        noduplicate_points = process(compressed_points)
        time_records.append(end_time - start_time)
        total_time += end_time - start_time
        compression_ratio = (1 - len(noduplicate_points) / len(points)) * 100
        compression_ratios.append(compression_ratio)
        #write_data.write(points, noduplicate_points, new_path, j)
        print(j)

    print(total_time)
    # timepath = r"F:\dataset\operbData\time0.csv"
    # compressRatio_path = r"F:\dataset\operbData\numbers0.csv"
    # write_data.write_time(time_records, compressRatio_path)
    # write_data.write_compressionRatio(compression_ratios, compressRatio_path)

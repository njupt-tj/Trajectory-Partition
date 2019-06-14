# -*- coding:utf-8 -*-
import math
import os
import time
import distances
import numpy as np
from point import Point
from read_data import read

'''
Bounded Quadrant System: Error-bounded
Trajectory Compression on the Go
'''


# 没有编号的点
class PointWithoutId:
    def __init__(self, x_coordinate, y_coordinate):
        self.__x = x_coordinate
        self.__y = y_coordinate

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y


# 线段类
class LineSegment:
    def __init__(self, start_p, end_p):
        self.__start_p = start_p
        self.__end_p = end_p

    def get_start(self):
        return self.__start_p

    def get_end(self):
        return self.__end_p

    def distance(self):
        return distances.point_distance(self.__start_p, self.__end_p)


# 边界矩形盒
class BoundingBox:
    '''
    边界矩形盒由四个顶点组成
    '''

    def __init__(self, origin_p, min_x, min_y, max_x, max_y):
        self.__origin_p = origin_p
        self.__left_top_p = PointWithoutId(min_x, max_y)
        self.__right_top_p = PointWithoutId(max_x, max_y)
        self.__right_bottom_p = PointWithoutId(max_x, min_y)
        self.__left_bottom_p = PointWithoutId(min_x, min_y)

    # 返回矩形边界盒
    def get_box(self):
        return [self.__left_top_p, self.__right_top_p, self.__right_bottom_p, self.__left_bottom_p]

    # 角度距离
    def corner_distance(self, cur_line_segment):
        start_point = cur_line_segment.get_start()
        end_point = cur_line_segment.get_end()
        dis_lt_ls = distances.perpendicular_distance(start_point, self.__left_top_p, end_point)
        dis_rt_ls = distances.perpendicular_distance(start_point, self.__right_top_p, end_point)
        dis_rb_ls = distances.perpendicular_distance(start_point, self.__right_bottom_p, end_point)
        dis_lb_ls = distances.perpendicular_distance(start_point, self.__left_bottom_p, end_point)
        return [dis_lt_ls, dis_rt_ls, dis_rb_ls, dis_lb_ls]

    # Near far corner distance
    def near_far_corner_distance(self, cur_line_segment):
        dis_lt_origin = distances.point_distance(self.__left_top_p, self.__origin_p)
        dis_rt_origin = distances.point_distance(self.__right_top_p, self.__origin_p)
        dis_rb_origin = distances.point_distance(self.__right_bottom_p, self.__origin_p)
        dis_lb_origin = distances.point_distance(self.__left_bottom_p, self.__origin_p)
        min_value = float('inf')
        max_value = 0
        min_index = 0
        max_index = 0
        four_dis = [dis_lt_origin, dis_rt_origin, dis_rb_origin, dis_lb_origin]
        for i in range(len(four_dis)):
            if four_dis[i] > max_value:
                max_value = four_dis[i]
                max_index = i
            if four_dis[i] < min_value:
                min_value = four_dis[i]
                min_index = i
        boxs = self.get_box()
        start_point = cur_line_segment.get_start()
        end_point = cur_line_segment.get_end()
        nearest_dis = distances.perpendicular_distance(start_point, boxs[min_index], end_point)
        farthest_dis = distances.perpendicular_distance(start_point, boxs[max_index], end_point)
        return [nearest_dis, farthest_dis]


# 最小角度和最大角度的边界线
class BoundingLines:
    def __init__(self, origin_p):
        self.__origin_p = origin_p

    def min_max_angle(self, bqs):
        min_angle = 2 * math.pi
        max_angle = 0
        min_angle_point = None
        max_angle_point = None
        for point in bqs:
            angle = distances.angle(self.__origin_p, point)
            if angle==-1:
                continue
            if angle <= min_angle:
                min_angle = angle
                min_angle_point = point
            if angle >= max_angle:
                max_angle = angle
                max_angle_point = point
        return [min_angle, min_angle_point, max_angle, max_angle_point]

    def get_lower_boundingline(self, min_angle_p, min_y, max_x, min_x):
        lower_k = (min_angle_p.get_y() - self.__origin_p.get_y()) / (min_angle_p.get_x() - self.__origin_p.get_x())
        lower_b = min_angle_p.get_y() - lower_k * min_angle_p.get_x()
        if lower_k == 0:
            l1_x = min_x
            l1_y = lower_b
            l2_x = max_x
            l2_y = lower_b
        else:
            l1_x = (min_y - lower_b) / lower_k
            l1_y = min_y
            l2_x = max_x
            l2_y = lower_k * max_x + lower_b
        l1 = PointWithoutId(l1_x, l1_y)
        l2 = PointWithoutId(l2_x, l2_y)
        return [l1, l2]

    def get_upper_boundingline(self, max_angle_p, min_x, max_y, max_x):
        upper_k = (max_angle_p.get_y() - self.__origin_p.get_y()) / (max_angle_p.get_x() - self.__origin_p.get_x())
        upper_b = max_angle_p.get_y() - upper_k * max_angle_p.get_x()
        if upper_k == 0:
            u1_x = min_x
            u1_y = upper_b
            u2_x = max_x
            u2_y = upper_b
        else:
            u1_x = min_x
            u1_y = min_x * upper_k + upper_b
            u2_x = (max_y - upper_b) / upper_k
            u2_y = max_y
        u1 = PointWithoutId(u1_x, u1_y)
        u2 = PointWithoutId(u2_x, u2_y)
        return [u1, u2]

    def get_boundinglines(self, min_y, max_x, min_x, max_y, bqs):
        result = self.min_max_angle(bqs)
        lower_boundingline = self.get_lower_boundingline(result[1], min_y, max_x, min_x)
        upper_boundingline = self.get_upper_boundingline(result[3], min_x, max_y, max_x)
        return lower_boundingline, upper_boundingline


# 获取嵌入距离
def get_intersection_distance(lower_boundingline, upper_boundingline, cur_linesegment):
    l1 = lower_boundingline[0]
    l2 = lower_boundingline[1]
    u1 = upper_boundingline[0]
    u2 = upper_boundingline[1]
    start_p = cur_linesegment.get_start()
    end_p = cur_linesegment.get_end()
    l1_ls_dis = distances.perpendicular_distance(start_p, l1, end_p)
    l2_ls_dis = distances.perpendicular_distance(start_p, l2, end_p)
    u1_ls_dis = distances.perpendicular_distance(start_p, u1, end_p)
    u2_ls_dis = distances.perpendicular_distance(start_p, u2, end_p)
    return [l1_ls_dis, l2_ls_dis, u1_ls_dis, u2_ls_dis]


# 获取线段的与x轴的角度
def get_linesegment_angle(cur_linesegment):
    return distances.angle(cur_linesegment.get_start(), cur_linesegment.get_end())


# 获取边界矩形范围
def get_corner_point(bqs):
    x_coordinates = []
    y_coordinates = []
    for point in bqs:
        x_coordinates.append(point.get_x())
        y_coordinates.append(point.get_y())
    x_coordinates.sort()
    y_coordinates.sort()
    return [x_coordinates[0], y_coordinates[0], x_coordinates[-1], y_coordinates[-1]]


# 计算bqs数量
def calc_bqs_numbers(buffered_points):
    first_quadrant = []
    second_quadrant = []
    third_quadrant = []
    fourth_quadrant = []
    for point in buffered_points:
        x = point.get_x()
        y = point.get_y()
        if x >= 0 and y >= 0:
            first_quadrant.append(point)
        elif x < 0 and y >= 0:
            second_quadrant.append(point)
        elif x < 0 and y < 0:
            third_quadrant.append(point)
        else:
            fourth_quadrant.append(point)
    bqss = []
    if len(first_quadrant) > 0:
        bqss.append(first_quadrant)
    if len(second_quadrant) > 0:
        bqss.append(second_quadrant)
    if len(third_quadrant) > 0:
        bqss.append(third_quadrant)
    if len(fourth_quadrant) > 0:
        bqss.append(fourth_quadrant)
    return bqss


# 判断一个点在第几象限
def get_quadrant(point):
    x = point.get_x()
    y = point.get_y()
    q = 0
    if x >= 0 and y >= 0:
        q = 1
    elif x >= 0 and y < 0:
        q = 4
    elif x < 0 and y >= 0:
        q = 2
    else:
        q = 3
    return q


# 判断是否在同一个象限
def is_same_quadrant(cur_linesegment, bqs):
    start_point = cur_linesegment.get_start()
    end_point = cur_linesegment.get_end()
    first_point = bqs[0]
    return get_quadrant(start_point) == get_quadrant(end_point) == get_quadrant(first_point)


# 计算偏差(包括lower bouned 和upper bouned)
def calc_deviation(origin_p, cur_linesegment, bqs):
    b = BoundingLines(origin_p)
    min_max_angles = b.min_max_angle(bqs)
    cur_linesegment_angle = get_linesegment_angle(cur_linesegment)
    corner_points = get_corner_point(bqs)
    boundlines = b.get_boundinglines(corner_points[1], corner_points[2], corner_points[0], corner_points[3], bqs)
    intersection_distances = get_intersection_distance(boundlines[0], boundlines[1], cur_linesegment)
    min_lower_dis = np.minimum(intersection_distances[0], intersection_distances[1])
    min_upper_dis = np.minimum(intersection_distances[2], intersection_distances[3])
    box = BoundingBox(origin_p, corner_points[0], corner_points[1], corner_points[2], corner_points[3])
    near_far_corner_distances = box.near_far_corner_distance(cur_linesegment)
    max_near_corner_disatnces = np.maximum(near_far_corner_distances[0], near_far_corner_distances[1])
    if (cur_linesegment_angle >= min_max_angles[0] and cur_linesegment_angle <= min_max_angles[2]) or \
            (is_same_quadrant(cur_linesegment, bqs) and (
                    cur_linesegment_angle > min_max_angles[2] or cur_linesegment_angle < min_max_angles[0])):
        d_lb = np.maximum(np.maximum(min_lower_dis, min_upper_dis), max_near_corner_disatnces)
        intersection_distances.sort()
        d_ub = intersection_distances[-1]
    elif is_same_quadrant(cur_linesegment, bqs) == False:
        min_upper_dis = np.minimum(intersection_distances[2], intersection_distances[1])
        corners_distance = box.corner_distance(cur_linesegment)
        corners_distance.sort()
        d_lb = np.maximum(np.maximum(min_lower_dis, min_upper_dis), corners_distance[0])
        d_ub = corners_distance[-1]
    return d_lb, d_ub


# 重新计算bqs中的点与当前线段的距离
def recalc_deviation(bqs, cur_linesegment):
    max_distance = 0
    start_p = cur_linesegment.get_start()
    end_p = cur_linesegment.get_end()
    for point in bqs:
        dis = distances.perpendicular_distance(start_p, point, end_p)
        if dis > max_distance:
            max_distance = dis
    return max_distance


# BQS压缩算法，传入参数为偏差阈值
def bqs(deviation_thr):
    s = 0
    buffered_points = []
    compressed_points.append(points[s])
    i = 1
    while i < len(points):
        dis = distances.point_distance(points[s], points[i])
        if dis <= deviation_thr:
            buffered_points.append(points[i])
        # 新的点可能导致更大的偏差，假设当前的线段为se
        else:
            e = i
            # 求bqs的个数
            if len(buffered_points) > 0:
                cur_linesegment = LineSegment(points[s], points[e])
                bqss = calc_bqs_numbers(buffered_points)
                max_d_lb = 0
                max_d_ub = 0
                for bqs in bqss:
                    d_lb, d_ub = calc_deviation(points[s], cur_linesegment, bqs)
                    if d_lb > max_d_lb:
                        max_d_lb = d_lb
                    if d_ub > max_d_ub:
                        max_d_ub = d_ub
                if max_d_ub <= deviation_thr:
                    buffered_points.append(points[e])
                elif max_d_lb > deviation_thr:
                    compressed_points.append(points[e - 1])
                    s = e - 1
                    # 清除缓存
                    buffered_points = []
                    buffered_points.append(points[e])
                elif deviation_thr >= max_d_lb and deviation_thr <= max_d_ub:
                    d = recalc_deviation(bqs, cur_linesegment)
                    # 根据d的值做决定
                    if d > deviation_thr:
                        compressed_points.append(points[e - 1])
                        s = e - 1
                        buffered_points = []
                        buffered_points.append(points[e])
                    else:
                        buffered_points.append(points[e])
            else:
                compressed_points.append(points[e])
                s = e

        i += 1


if __name__ == '__main__':
    # 读取轨迹数据
    tradata = []
    # 文件目录路径
    raw_path = r"F:\dataset\rawData\0"
    new_path = r"F:\dataset\bqsData\0"
    file_list = os.listdir(raw_path)
    file_list.sort(key=lambda x: x[10:-5])
    # 读取每个文件的轨迹数据
    for i in range(len(file_list)):
        tradata.append(read(raw_path, file_list[i]))
    time_records = []
    compression_ratios = []
    error_bound = 10
    total_time = 0
    for j in range(len(tradata)):
        id = 0
        points = []
        for point in tradata[j]:
            p = Point(id, point[0], point[1], point[2])
            points.append(p)
            id = id + 1
        compressed_points = []
        # 传入参数：5:压缩比
        start_time = time.clock()
        bqs(error_bound)
        end_time = time.clock()
        compressed_points.append(points[-1])
        time_records.append(end_time - start_time)
        total_time += end_time - start_time
        cmp_ratio = (1 - len(compressed_points) / len(points)) * 100
        compression_ratios.append(cmp_ratio)
        #write_data.write(compressed_points, new_path, j)
        print(j)

    print(total_time)
    # timepath = r"F:\dataset\bqsData\time0.csv"
    # compressRatio_path = r"F:\dataset\bqsData\numbers0.csv"
    # write_data.write_time(time_records, compressRatio_path)
    # write_data.write_compressionRatio(compression_ratios, compressRatio_path)

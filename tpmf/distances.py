# -*- coding:utf-8 -*-
import math

import numpy as np

'''
定义各种距离函数
'''


# 计算点之间的距离,返回的是meters
def point_distance(p1, p2):
    x_diff = p1.get_x() - p2.get_x()
    y_diff = p1.get_y() - p2.get_y()
    return np.sqrt(x_diff * x_diff + y_diff * y_diff) * 1000


# 计算两个点之间的时间间隔
def time_interval(p1, p2):
    import datetime
    s1 = '%s %s' % ('2019-6-3', p1.get_t())
    s2 = '%s %s' % ('2019-6-3', p2.get_t())
    # 字符串转时间格式
    d1 = datetime.datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(s2, '%Y-%m-%d %H:%M:%S')
    return (d2 - d1).total_seconds()


# 计算两个连续点的之间的移动速度
def calculate_speed(p1, p2):
    xy_distance = point_distance(p1, p2)
    xy_interval = time_interval(p1, p2)
    return xy_distance / xy_interval


# 计算垂直欧式距离PED
def perpendicular_distance(start_p, middle_p, end_p):
    se_distance = point_distance(start_p, end_p)
    sm_distance = point_distance(start_p, middle_p)
    em_distance = point_distance(middle_p, end_p)
    if se_distance == 0:
        return sm_distance
    elif sm_distance == 0 or em_distance == 0:
        return 0
    else:
        p = (se_distance + sm_distance + em_distance) / 2
        S = math.sqrt(math.fabs(p * (p - se_distance) * (p - sm_distance) * (p - em_distance)))
        return (2 * S) / se_distance


# 计算时间同步距离SED
def sed_distance(left_point, middle_point, right_point):
    ml_time_diff = time_interval(left_point, middle_point)
    ls_time_diff = time_interval(left_point, right_point)
    if ls_time_diff == 0:
        time_ratio = 1
    else:
        time_ratio = ml_time_diff / ls_time_diff
    new_x = left_point.get_x() + (right_point.get_x() - left_point.get_x()) * time_ratio
    new_y = left_point.get_y() + (right_point.get_y() - left_point.get_y()) * time_ratio
    x_diff = middle_point.get_x() - new_x
    y_diff = middle_point.get_y() - new_y
    return math.sqrt(x_diff * x_diff + y_diff * y_diff)*1000

#线段与x轴的夹角
def angle(first_point,second_point):
    x_diff=second_point.get_x()-first_point.get_x()
    y_diff=second_point.get_y()-first_point.get_y()
    angle=math.atan(y_diff/x_diff)
    return angle

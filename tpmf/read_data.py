# -*- coding:utf-8 -*-
import os
import csv

#读取单个文件的轨迹数据
def read(path,filename):
    file = os.path.join(path, filename)
    data = []
    # 读取数据文件，并保存到data
    with open(file, 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            data.append(line)

    # data将集合里的字符串类型转换成数值类型
    for point in data:
        point[0] = float(point[0])
        point[1] = float(point[1])
    return data
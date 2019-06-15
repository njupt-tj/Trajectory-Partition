# -*- coding:utf-8 -*-

import os
import csv
import pandas


def write1(raw_points, compressed_points, path, number):
    filename = "trajectory" + str(number)+".csv"
    file_path = os.path.join(path, filename)
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for i in compressed_points:
            row = [raw_points[i].get_x(), raw_points[i].get_y(), raw_points[i].get_t()]
            writer.writerow(row)


def write(compressed_points, path, number):
    filename = "trajectory" + str(number)+".csv"
    file_path = os.path.join(path, filename)
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for point in compressed_points:
            row = [point.get_x(), point.get_y(), point.get_t()]
            writer.writerow(row)


def write_time(time_reocrds, path):
    writer = pandas.DataFrame({'time': time_reocrds})
    writer.to_csv(path, index=False)


def write_compressionRatio(compression_ratios, path):
    writer = pandas.DataFrame({'compression_ratio': compression_ratios})
    writer.to_csv(path, index=False)

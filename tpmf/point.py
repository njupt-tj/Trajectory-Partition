# -*- coding:utf-8 -*-

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

    def get_id(self):
        return self.__id

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_t(self):
        return self.__t
# -*- coding:utf-8 -*-
import numpy as np


def calculatePerpendDis(a, b, abDis, c, d, cdDis):
    """计算垂直距离"""
    acDis = np.sqrt(np.sum(np.square(c - a))) * 1000
    adDis = np.sqrt(np.sum(np.square(d - a))) * 1000
    bcDis = np.sqrt(np.sum(np.square(c - b))) * 1000
    bdDis = np.sqrt(np.sum(np.square(d - b))) * 1000
    if abDis <= cdDis:
        p1 = (acDis + adDis + cdDis * 1000) / 2
        p2 = (bcDis + bdDis + cdDis * 1000) / 2
        s1 = math.sqrt(math.fabs(p1 * (p1 - acDis) * (p1 - adDis) * (p1 - cdDis * 1000)))
        s2 = math.sqrt(math.fabs(p2 * (p2 - bcDis) * (p2 - bdDis) * (p2 - cdDis * 1000)))
        l1 = (2 * s1) / (cdDis * 1000)
        l2 = (2 * s2) / (cdDis * 1000)
        if (l1 + l2) == 0:
            return 0
        else:
            return (l1 * l1 + l2 * l2) / (l1 + l2)
    else:
        p1 = (acDis + bcDis + abDis * 1000) / 2
        p2 = (adDis + bdDis + abDis * 1000) / 2

        s1 = math.sqrt(math.fabs(p1 * (p1 - acDis) * (p1 - bcDis) * (p1 - abDis * 1000)))
        s2 = math.sqrt(math.fabs(p2 * (p2 - adDis) * (p2 - bdDis) * (p2 - abDis * 1000)))

        l1 = (2 * s1) / (abDis * 1000)
        l2 = (2 * s2) / (abDis * 1000)
        if (l1 + l2) == 0:
            return 0
        else:
            return (l1 * l1 + l2 * l2) / (l1 + l2)


def calculateHorizontalDis(a, b, abDis, c, d, cdDis):
    """计算水平距离"""
    if abDis <= cdDis:
        ca = a - c
        cd = d - c
        caDis = np.sqrt(np.sum(np.square(a - c)))
        if caDis == 0:
            h1 = 0
        else:
            h1 = caDis * 1000 * math.fabs(np.dot(ca, cd) / (caDis * cdDis))
        db = b - d
        dc = -cd
        dbDis = np.sqrt(np.sum(np.square(b - d)))
        if dbDis == 0:
            h2 = 0
        else:
            h2 = dbDis * 1000 * math.fabs(np.dot(db, dc) / (dbDis * cdDis))
        return max(h1, h2)
    else:
        ac = c - a
        ab = b - a
        acDis = np.sqrt(np.sum(np.square(a - c)))
        if acDis == 0:
            h1 = 0
        else:
            h1 = acDis * 1000 * math.fabs(np.dot(ac, ab) / (acDis * abDis))
        bd = d - b
        ba = -ab
        bdDis = np.sqrt(np.sum(np.square(b - d)))
        if bdDis == 0:
            h2 = 0
        else:
            h2 = bdDis * 1000 * math.fabs(np.dot(bd, ba) / (bdDis * abDis))
        return max(h1, h2)


def calculate_interval(t1, t2):
    """计算时间间隔"""
    import datetime
    s1 = '2018-3-22' + ' ' + t1
    s2 = '2018-3-22' + ' ' + t2
    # 字符串转时间格式
    d1 = datetime.datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(s2, '%Y-%m-%d %H:%M:%S')
    return (d2 - d1).total_seconds()


# 计算时间距离
def calculateTimeDis(X, Y):
    """计算时间距离"""
    ab_t1 = X[0][2]
    ab_t2 = X[1][2]

    cd_t1 = Y[0][2]
    cd_t2 = Y[1][2]

    # 比较时间大小
    seconds1 = calculate_interval(ab_t1, cd_t1)
    seconds2 = calculate_interval(ab_t2, cd_t2)

    if seconds1 > 0:
        interval1 = seconds1 / 3600
    else:
        interval1 = (-seconds1) / 3600

    if seconds2 > 0:
        interval2 = seconds2 / 3600
    else:
        interval2 = (-seconds2) / 3600
    return math.sqrt(interval1 * interval1 + interval2 * interval2)


if __name__ == '__main__':
    # 读取所有的轨迹段数据
    import os

    file_dir = r"C:\Users\TJ\Desktop\Dataset\Geolife Trajectories 1.3\Feature_Trajectory\0"
    file_list = os.listdir(file_dir)
    file_list.sort(key=lambda fn: os.path.getatime(file_dir + "\\" + fn))
    # 一个用户的所有划分后的轨迹段数据
    allData = []
    eachfileData = []
    clusters = []
    for eachFile in file_list:
        # 读取每个文件中的数据
        fileName = os.path.join(file_dir, eachFile)
        with open(fileName, 'r') as f:
            import csv

            reader = csv.reader(f)
            for rawData in reader:
                eachfileData.append(rawData)
            allData.append(eachfileData)
            eachfileData = []

    # 类型转换
    for eachTra in allData:
        for data in eachTra:
            data[0] = float(data[0])
            data[1] = float(data[1])

    allSegments = []
    S = []
    for D in allData:
        for i in range(len(D) - 1):
            S.append(D[i])
            S.append(D[i + 1])
            allSegments.append(S)
            S = []

    # 去除过距离为0的轨迹段
    for item in allSegments:
        a = np.array(item[0][:2])
        b = np.array(item[1][:2])
        dis = np.sqrt(np.sum(np.square(a - b))) * 1000
        if dis == 0:
            allSegments.remove(item)

    perDist=[]
    hisDist=[]
    timeDist=[]
    for i in range(len(allSegments)-1):
        a=np.array(allSegments[i][0][:2])
        b=np.array(allSegments[i][1][:2])
        c=np.array(allSegments[i+1][0][:2])
        d=np.array(allSegments[i+1][1][:2])
        abdis=np.sqrt(np.sum(np.square(a-b)))
        cddis=np.sqrt(np.sum(np.square(d-c)))
        perDist.append(calculatePerpendDis(a,b,abdis,c,d,cddis))
        hisDist.append(calculateHorizontalDis(a,b,abdis,c,d,cddis))
        timeDist.append(allSegments[i],allSegments[i+1])

    print("最小最大垂直距离：",end="")
    print(min(perDist),end="")
    print(max(perDist))
    print("最小最大水平距离：", end="")
    print(min(hisDist), end="")
    print(max(hisDist))
    print("最小最大时间距离：", end="")
    print(min(timeDist), end="")
    print(max(timeDist))
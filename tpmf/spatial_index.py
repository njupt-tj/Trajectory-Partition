# -*- coding:utf-8 -*-


def timeRank(allSegments):
    """对轨迹段时间排序"""
    sortedSegments=sorted(allSegments, key=lambda x:(x[0][2],x[1][2]))
    # print(sortedSegments[152])
    return sortedSegments
    # timeIndex = []
    # i = 0  # 每个轨迹段最初的索引
    # temp = []
    # for segment in allSegments:
    #     temp.append(segment[0][2])
    #     temp.append(segment[1][2])
    #     temp.append(i)
    #     timeIndex.append(temp)
    #     temp = []
    #     i = i + 1
    # timeIndex = sorted(timeIndex, key=itemgetter(0, 1))
    # print(time+timedelta(minutes=30))

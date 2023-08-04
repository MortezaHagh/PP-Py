from math import sqrt


def cal_distance(x1, y1, x2, y2, type):
    if type == 'euclidean':
        dist = round(sqrt((x1-x2)**2+(y1-y2)**2), 5)
    elif type == 'manhattan':
        dist = abs(x1-x2) + abs(y1-y2)
    return dist

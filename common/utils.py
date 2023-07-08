import numpy as np
from cmath import sqrt


class Utils:
    def __init__(self, dis_type="euclidean"):
        self.dis_type = dis_type

    def cal_distance(self, x1, y1, x2, y2):
        if self.dis_type == 'euclidean':
            dist = sqrt((x1-x2)**2+(y1-y2)**2)
        elif self.dis_type == 'manhattan':
            dist = abs(x1-x2) + abs(y1-y2)
        return dist

    def angle_diff(self, ang1, ang2):
        da = ang1-ang2
        da = np.arctan2(np.sin(da), np.cos(da))
        return da

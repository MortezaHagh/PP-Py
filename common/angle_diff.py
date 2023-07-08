import numpy as np


def angle_diff(ang1, ang2):
    da = ang1-ang2
    da = np.arctan2(np.sin(da), np.cos(da))
    return da

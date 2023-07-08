import numpy as np
from angle_diff import angle_diff


def cal_smoothness(path):

    dirs = path.dirs
    nodes = path.nodes
    dn = np.diff(nodes)
    dirs = np.array(dirs)
    dirs2 = dirs[np.where(dn != 0)]
    d_theta = [angle_diff(dirs2[i], dirs2[i-1]) for i in range(1, len(dirs2))]
    smoothness = sum(np.abs(d_theta))

    return smoothness

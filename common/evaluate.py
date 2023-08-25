import csv
import numpy as np
from common.angle_diff import angle_diff


class Evaluate:
    def __init__(self, pp_obj, method):
        self.sol = pp_obj.sol
        self.max_steps = len(self.sol.nodes)
        self.path_length = round(self.cal_cost(), 2)
        self.smoothness = round(self.cal_smoothness(), 2)
        self.path_turns = round(self.smoothness/(np.pi/2), 2)

        # statistics
        self.proc_time = pp_obj.sol.proc_time
        self.n_closed = pp_obj.n_closed
        self.n_opened = pp_obj.n_opened
        self.n_expanded = pp_obj.n_expanded
        self.n_reopened = pp_obj.n_reopened
        self.n_final_open = pp_obj.n_final_open

        #
        self.record(method)

    def cal_cost(self):
        dxPath = np.diff(self.sol.x)
        dyPath = np.diff(self.sol.y)
        dxPath2 = np.power(dxPath, 2)
        dyPath2 = np.power(dyPath, 2)
        path_length = sum(np.sqrt(np.add(dxPath2, dyPath2)))
        return path_length

    def cal_smoothness(self):
        dirs = self.sol.dirs
        nodes = self.sol.nodes
        dn = np.diff(nodes)
        dirs = np.array(dirs)
        dirs2 = dirs[np.where(dn != 0)]
        d_theta = [angle_diff(dirs2[i], dirs2[i-1])
                   for i in range(1, len(dirs2))]
        smoothness = sum(np.abs(d_theta))
        return smoothness

    def record(self, method):
        csv_path = "/home/piotr/dev/MRPP/PathPlanningPy/result.csv"
        with open(csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([method, self.max_steps, self.path_length, self.smoothness, self.path_turns, self.proc_time, 
                             self.n_expanded, self.n_opened, self.n_reopened, self.n_final_open])

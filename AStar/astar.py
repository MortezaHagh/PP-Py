import time
import numpy as np
from support import Open, Sol
from support import Closed, TopNode
from common.angle_diff import angle_diff
from common.cal_distance import cal_distance


class AStar:
    def __init__(self, model):

        # initialize
        self.model = model
        self.closed = Closed()
        top_node = self.create_top_node()
        self.open = Open(top_node)
        self.closed.count += 1
        self.closed.nodes.append(top_node.node)
        self.top_node = top_node

        # start process time
        self.end_time = 0
        start_time = time.process_time()

        # astar
        self.astar()

        # end process time
        self.end_time = time.process_time()
        self.sol.proc_time = self.end_time - start_time

    # ------------------------------------------------------------

    def astar(self):
        while self.top_node.node != self.model.robot.goal_node:

            # finding neighbors (successors)
            feas_neighbors = self.expand()

            # update or extend Open list with the successor nodes
            self.update_open(feas_neighbors)

            # select new Top Node
            self.select_top_node()

        self.end_time = time.process_time()
        self.create_sol()

    # ------------------------------------------------------------

    def expand(self):
        feas_neighbors = []
        neghbors = self.model.neighbors[self.top_node.node]
        for neigh in neghbors:
            if neigh not in self.closed.nodes:
                feas_neighb = TopNode()
                feas_neighb.dir = neigh.dir
                feas_neighb.node = neigh.node
                feas_neighb.p_node = self.top_node.node
                feas_neighb.g_cost = self.top_node.g_cost + neigh.cost
                h_cost = cal_distance(
                    self.model.robot.xt, self.model.robot.yt, neigh.x, neigh.y, self.model.dist_type)
                feas_neighb.f_cost = feas_neighb.g_cost + h_cost
                feas_neighbors.append(feas_neighb)
        return feas_neighbors

    def update_open(self, neighbors):
        for neigh in neighbors:
            if neigh in self.open.nodes:
                ind = self.open.nodes.index(neigh)
                if neigh.f_cost < self.open.list[ind].f_cost:
                    self.open.list[ind] = neigh
            else:
                self.open.count += 1
                neigh.ind = self.open.count
                self.open.list.append(neigh)
                self.open.nodes.append(neigh.node)

    def select_top_node(self):
        inds = [op.ind for op in self.open.list if not op.visited]
        if len(inds) < 0:
            print(" error: Astar failed to find a path, impossible!")
            raise

        f_costs = [self.open.list[ind].f_cost for ind in inds]
        if self.model.expand_method == 'random':
            min_ind = np.argmin(f_costs)
        elif self.model.expand_method == 'heading':
            dtheta = [abs(angle_diff(self.top_node.dir, self.open.list[ind].dir)) for ind in inds]
            costs = [dtheta, f_costs]
            sorted_inds = np.lexsort(costs)
            min_ind = sorted_inds[0]
        self.open.list[min_ind].visited = True
        self.top_node = self.open.list[min_ind]

    def final_path_nodes(self):
        i = 0
        path_nodes = []
        node_number = self.model.robot.goal_node
        path_nodes.append(node_number)

        path_nodes.reverse()
        return path_nodes

    # ------------------------------------------------------------

    def turn_cost(self, preds, node, current_dir):
        dtheta = []
        y = self.model.nodes.y[node]
        x = self.model.nodes.x[node]
        for i in preds:
            dy = self.model.nodes.y[i]-y
            dx = self.model.nodes.x[i]-x
            theta = np.arctan2(dy, dx)
            dt = np.arctan2(np.sin(theta-current_dir),
                            np.cos(theta-current_dir))
            dtheta.append(dt)
        return dtheta

    # ------------------------------------------------------------

    def create_top_node(self):
        top_node = TopNode()
        top_node.ind = 0
        top_node.visited = True
        top_node.dir = self.model.robot.dir
        top_node.node = self.model.robot.start_node
        top_node.p_node = self.model.robot.start_node
        h_cost = cal_distance(self.model.robot.xs, self.model.robot.ys,
                              self.model.robot.xt, self.model.robot.yt, self.model.dist_type)
        top_node.g_cost = 0
        top_node.f_cost = h_cost

        return top_node

    def create_sol(self):
        sol = Sol()
        sol.nodes = self.path_nodes
        sol.x = [self.model.nodes.x[i] for i in self.path_nodes]
        sol.y = [self.model.nodes.y[i] for i in self.path_nodes]
        sol.dirs = self.node_to_dir(self.path_nodes)
        self.sol = sol

    def node_to_dir(self, nodes):
        dirs = []
        for i in range(1, len(nodes)):
            x1 = self.model.nodes.x[nodes[i-1]]
            y1 = self.model.nodes.y[nodes[i-1]]
            x2 = self.model.nodes.x[nodes[i]]
            y2 = self.model.nodes.y[nodes[i]]
            dy = y2-y1
            dx = x2-x1
            theta = np.arctan2(dy, dx)
            theta = round(theta, 3)
            dirs.append(theta)

        dirs.append(dirs[-1])
        return dirs

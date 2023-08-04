import time
import numpy as np
from support import Open, Sol
from support import Closed, TopNode
from common.angle_diff import angle_diff
from common.cal_distance import cal_distance
from heapq import heappush, heappop
from common.plotting import Plotter


class EPEAStar:
    def __init__(self, model):

        # settings
        self.dir_coeff = 0.0
        self.do_plot = False  # True False

        # stats
        self.n_closed = 0
        self.n_opened = 0
        self.n_expanded = 0
        self.n_reopened = 0
        self.n_final_open = 0

        # initialize
        self.FN = np.inf
        self.model = model
        self.closed = Closed()
        top_node = self.create_top_node()
        self.top_node = top_node
        self.closed = [0 for i in range(model.nodes.count)]
        self.parents = [-1 for i in range(model.nodes.count)]
        self.fcost = [-1 for i in range(model.nodes.count)]
        self.fcost[top_node.node] = top_node.f_cost
        self.parents[top_node.node] = top_node.p_node
        # self.closed[top_node.node] = 1

        # plot
        if self.do_plot:
            plot_dyno = False  # False True
            self.plotter = Plotter(model, plot_dyno)
            self.plotter.update1(self.top_node.node)

        self.heap_open = []
        self.heap_open = [((top_node.f_cost, top_node.h_cost, self.n_opened), top_node)]

        # start process time
        self.end_time = 0
        start_time = time.process_time()

        # astar
        self.astar()

        # end process time
        self.sol.proc_time = self.end_time - start_time

    # ------------------------------------------------------------

    def astar(self):
        while self.top_node.node != self.model.robot.goal_node:
            
            # select new Top Node
            self.select_top_node()

            # finding neighbors (successors)
            feas_neighbors = self.expand()

            # update or extend Open list with the successor nodes
            self.update_open(feas_neighbors)

             # plot
            if self.do_plot:
                o_nodes = [o[1].node for o in self.heap_open]
                self.plotter.update2(self.top_node.node, o_nodes)


        # optimal paths
        self.path_nodes = self.optimal_path()

        # create sol
        self.end_time = time.process_time()
        self.create_sol()
        self.n_closed = sum(self.closed)
        self.n_final_open = len(self.heap_open)

    # ------------------------------------------------------------

    def expand(self):
        self.FN = np.inf
        feas_neighbors = []
        neghbors = self.model.neighbors[self.top_node.node]
        for neigh in neghbors:
            if neigh.node == self.top_node.p_node:
                continue
            if (self.closed[neigh.node] == 0):
                feas_neighb = TopNode()
                feas_neighb.dir = neigh.dir
                feas_neighb.node = neigh.node
                feas_neighb.p_node = self.top_node.node
                feas_neighb.dir_cost = int(not (self.top_node.dir - neigh.dir) == 0)*self.dir_coeff
                feas_neighb.g_cost = self.top_node.g_cost + neigh.cost + feas_neighb.dir_cost
                feas_neighb.h_cost = cal_distance(self.model.robot.xt, self.model.robot.yt, neigh.x, neigh.y, self.model.dist_type)
                feas_neighb.f_cost = feas_neighb.g_cost + feas_neighb.h_cost*1
                if round(feas_neighb.f_cost, 5) != round(self.top_node.f_cost, 5):
                    if round(feas_neighb.f_cost, 5) > round(self.top_node.f_cost, 5):
                        self.FN = min(self.FN, feas_neighb.f_cost)
                else:
                    self.n_expanded += 1
                    heappush(feas_neighbors, ((feas_neighb.f_cost, self.n_expanded), feas_neighb))
        return feas_neighbors

    def update_open(self, neighbors):
        if len(neighbors)==0:
            self.closed[self.top_node.node] = 1
        while len(neighbors) > 0:
            c, neigh = heappop(neighbors)
            open_flag = False
            if self.fcost[neigh.node] > 0:
                if neigh.f_cost < self.fcost[neigh.node]:
                    open_flag = True
                    self.n_reopened += 1
            else:
                open_flag = True

            if open_flag:
                self.n_opened += 1
                self.fcost[neigh.node] = neigh.f_cost
                self.parents[neigh.node] = neigh.p_node
                heappush(self.heap_open, ((neigh.f_cost, neigh.h_cost, -self.n_opened), neigh))

        if self.FN is np.inf:
            self.closed[self.top_node.node] = 1
        else:
            self.n_opened += 1
            self.n_reopened += 1
            # self.fcost[self.top_node.node] = self.FN
            self.top_node.f_cost = self.FN
            heappush(self.heap_open, ((self.top_node.f_cost, self.top_node.h_cost, self.n_opened), self.top_node))

    def select_top_node(self):
        c, top_node = heappop(self.heap_open)
        self.top_node = top_node
        # self.closed[top_node.node] = 1

    def optimal_path(self):
        path_nodes = [self.model.robot.goal_node]
        parent_node = self.top_node.p_node
        while parent_node != self.model.robot.start_node:
            path_nodes.append(parent_node)
            parent_node = self.parents[parent_node]

        path_nodes.append(self.model.robot.start_node)
        path_nodes.reverse()
        return path_nodes

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
        top_node.h_cost = h_cost
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

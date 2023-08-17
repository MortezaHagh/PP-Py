import time
import numpy as np
from heapq import heappush, heappop
from common.plotting import Plotter
from common.cal_distance import cal_distance
from AStar.support import Closed, TopNode, Sol


class AStar:
    def __init__(self, model):

        # settings
        self.dir_coeff = 0.0
        self.from_start = True
        self.do_plot = False  # True False

        # stats
        self.n_closed = 0
        self.n_opened = 0
        self.n_expanded = 0
        self.n_reopened = 0
        self.n_final_open = 0

        # initialize
        if self.from_start:
            self.start = model.start
            self.goal = model.goal
        else:
            self.goal = model.start
            self.start = model.goal
        self.model = model
        self.closed = Closed()
        top_node = self.create_top_node()
        self.top_node = top_node
        self.closed = [0 for i in range(model.nodes.count)]
        self.parents = [-1 for i in range(model.nodes.count)]
        self.fcost = [-1 for i in range(model.nodes.count)]
        self.fcost[top_node.node] = top_node.f_cost
        self.parents[top_node.node] = top_node.p_node
        self.closed[top_node.node] = 1

        # plot
        if self.do_plot:
            self.o_nodes = []
            plot_dyno = False  # False True
            self.plotter = Plotter(model, plot_dyno)
            self.plotter.update1(self.top_node.node)

        self.heap_open = [((top_node.f_cost, -top_node.g_cost, self.n_opened), top_node)]

        # start process time
        self.end_time = 0
        start_time = time.process_time()

        # astar
        self.astar()

        # end process time
        self.sol.proc_time = self.end_time - start_time

    # ------------------------------------------------------------

    def astar(self):
        while self.top_node.node != self.goal.node:

            # select new Top Node
            self.select_top_node()

            # finding neighbors (successors)
            feas_neighbors = self.expand()

            # update or extend Open list with the successor nodes
            self.update_open(feas_neighbors)

            # plot
            if self.do_plot:
                self.plotter.update2(self.top_node.node, self.o_nodes)
                self.o_nodes = []

        # optimal paths
        self.path_nodes = self.optimal_path()

        # create sol
        self.end_time = time.process_time()
        self.create_sol()
        self.n_closed = sum(self.closed)
        self.n_final_open = len(self.heap_open)

    # ------------------------------------------------------------

    def expand(self):
        feas_neighbors = []
        neghbors = self.model.neighbors[self.top_node.node]
        for neigh in neghbors:
            if neigh.node == self.top_node.p_node:
                continue
            if (self.closed[neigh.node] == 0):
                self.n_expanded += 1
                feas_neighb = TopNode()
                feas_neighb.dir = neigh.dir
                feas_neighb.node = neigh.node
                feas_neighb.p_node = self.top_node.node
                feas_neighb.dir_cost = int(not (self.top_node.dir - neigh.dir) == 0)*self.dir_coeff
                feas_neighb.g_cost = self.top_node.g_cost + neigh.cost + feas_neighb.dir_cost
                feas_neighb.h_cost = cal_distance(self.goal.x, self.goal.y, neigh.x, neigh.y, self.model.dist_type)
                feas_neighb.f_cost = feas_neighb.g_cost + feas_neighb.h_cost*1
                feas_neighbors.append(feas_neighb)
        return feas_neighbors

    def update_open(self, neighbors):
        if neighbors == []:
            return

        for neigh in neighbors:
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
                heappush(self.heap_open, ((neigh.f_cost, -neigh.g_cost, -self.n_opened), neigh))

                if self.do_plot:
                    self.o_nodes.append(neigh.node)

    def select_top_node(self):
        c, top_node = heappop(self.heap_open)
        self.top_node = top_node
        self.closed[top_node.node] = 1

    def optimal_path(self):
        path_nodes = [self.goal.node]
        parent_node = self.top_node.p_node
        while parent_node != self.start.node:
            path_nodes.append(parent_node)
            parent_node = self.parents[parent_node]

        path_nodes.append(self.start.node)
        if self.from_start:
            path_nodes.reverse()
        return path_nodes

    # ------------------------------------------------------------

    def create_top_node(self):
        top_node = TopNode()
        top_node.visited = True
        top_node.dir = self.start.dir
        top_node.node = self.start.node
        top_node.p_node = self.start.node
        h_cost = cal_distance(self.start.x, self.start.y, self.goal.x, self.goal.y, self.model.dist_type)
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

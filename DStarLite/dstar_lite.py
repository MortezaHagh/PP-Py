import numpy as np
from support import Open, Sol
from support import Start, TopNode
from update_map import update_map
from common.cal_distance import cal_distance


class DStarLite:
    def __init__(self, model):
        # initialize
        RHS = model.RHS
        RHS[top_node.node] = 0
        top_node = self.create_top_node()
        self.open = Open(top_node)
        self.G = model.G
        self.RHS = model.RHS
        self.model = model

        # start
        self.current_dir = self.model.robot.dir
        self.path_nodes = [self.model.robot.start_node]
        self.start = self.create_start()

        # dstar_lite
        self.dstar_lite()

    # ------------------------------------------------------------

    def dstar_lite(self):
        t = 1

        # compute shortest path
        # [G, RHS, open, start] (G, RHS, open, start, self.model)
        self.compute_shortest_path()

        # # main procedure
        while self.start.node != self.model.robot.goal_node:
            # move robot to next node
            succ = self.model.successors[self.start.node]
            succ_c = self.model.succ_cost[self.start.node]
            succ_g = np.array(self.G[succ])
            if self.model.expand_method == 'random':
                min_ind = np.argmin(succ_c+succ_g)
                self.start.node = succ[min_ind]
            elif self.model.expand_method == 'heading':
                dtheta = self.turn_cost(succ)
                c1 = succ_c+succ_g
                c2 = [np.abs(dtheta), c1]
                c3 = np.array(c2)
                inds = np.lexsort(c3)
                self.start.node = succ[inds[0]]
                current_dir = current_dir + dtheta[inds[0]]

            self.start.x = self.model.nodes.x[self.start.node]
            self.start.y = self.model.nodes.y[self.start.node]

            # move to start.node and add start.node to Path
            t = t+1
            self.path_nodes.append(self.start.node)

            # # check for update in edge costs (obstacles)
            # [open, RHS, model] = update_map(open, RHS, G, model, start, t)

            # compute shortest path
            self.compute_shortest_path()

        self.create_sol()

    # ------------------------------------------------------------

    def compute_shortest_path(self):

        # select top key
        self.top_key()

        # update start_key
        c = min(self.G[self.start.node], self.RHS[self.start.node])
        self.start.key = [c+self.model.km, c]

        while self.compare_keys(self.top_node.key, self.start.key) or self.RHS[self.start.node] != self.G[self.start.node]:
            k_old = self.top_node.key
            k_new = min(self.G[self.top_node.node], self.RHS[self.top_node.node]) + \
                np.array([self.top_node.h_cost+self.model.km, 0])

            # remove topkey from open
            self.open.list.pop(self.top_node.ind)
            self.open.count = self.open.count - 1

            # update vertex
            update_list = self.model.predecessors[self.top_node.node]
            if self.compare_keys(k_old, k_new):
                self.open.list.append(self.top_node)
                self.open.list[-1].key = k_new
                self.open.count += 1
            else:
                if self.G[self.top_node.node] > self.RHS[self.top_node.node]:
                    self.G[self.top_node.node] = self.RHS[self.top_node.node]
                else:
                    self.G[self.top_node.node] = np.inf
                    update_list.append(self.top_node.node)
                self.update_vertex(update_list)

            # select top key
            self.top_key()

            # update start_key
            c = min(self.G[self.start.node], self.RHS[self.start.node])
            self.start.key = [c+self.model.km, c]

    # ------------------------------------------------------------

    def top_key(self):
        keys = np.array([[np.random.rand(1)[-1], op.key[1], op.key[0]]
                        for op in self.open.list])
        ind = np.lexsort(keys.T)
        top_node = self.open.list[ind[0]]
        top_node.ind = ind[0]
        self.top_node = top_node

    def turn_cost(self, succ):
        dtheta = []
        y = self.model.nodes.y[self.start.node]
        x = self.model.nodes.x[self.start.node]
        for i in succ:
            dy = self.model.model.nodes.y[i]-y
            dx = self.model.model.nodes.x[i]-x
            theta = np.arctan2(dy, dx)
            dt = np.arctan2(np.sin(theta-self.current_dir),
                            np.cos(theta-self.current_dir))
            dtheta.append(dt)
        return dtheta

    def compare_keys(self, key1, key2):
        result = True
        if key1[0] > key2[0]:
            result = False
        elif key1[0] == key2[0]:
            if key1[1] >= key2[1]:
                result = False
        return result

    def update_vertex(self, update_list):
        for inode in update_list:
            if inode != self.model.robot.goal_node:
                succ = self.model.successors[inode]
                succ_c = self.model.succ_cost[inode]
                succ_g = np.array(self.G[succ])
                self.RHS[inode] = min(succ_g+succ_c)

            open_nodes = [op.node for op in self.open.list]
            if inode in open_nodes:
                ind = open_nodes.index(inode)
                self.open.list.pop(ind)
                self.open.count -= 1

            if self.G[inode] != self.RHS[inode]:
                self.open.count += 1
                op = TopNode()
                op.node = inode
                x = self.model.nodes.x[inode]
                y = self.model.nodes.y[inode]
                op.h_cost = cal_distance(
                    self.start.x, self.start.y, x, y, self.model.dist_type)
                c = min(self.G[inode], self.RHS[inode])
                op.key = [c+self.model.km+op.h_cost, c]
                op.ind = self.open.count
                self.open.list.append(op)

    # def update_map(open, RHS, G, model, start, t):
    #     if t == 2:
    #         new_obst_node = 31
    #         for ind, node in enumerate(model.predecessors[new_obst_node]):
    #             model.pred_cost[new_obst_node][ind] = np.inf
    #             suc_ind = np.where(new_obst_node==model.successors[node])
    #             model.succ_cost[node][suc_ind] = np.inf

    #         xl = model.nodes.x[model.s_last]
    #         yl = model.nodes.y[model.s_last]
    #         model.km = model.km + \
    #             cal_distance(xl, yl, start.x, start.y, model.dist_type)
    #         model.s_last = start.node
    #         update_list = model.predecessors[new_obst_node]

    #         # update vertex
    #         [open, RHS] = update_vertex(open, RHS, G, update_list, model, start)

    #     return open, RHS, model

    # ------------------------------------------------------------

    def create_start(self):
        start = Start()
        start.node = self.model.robot.start_node
        self.key = [min(self.G[start.node], self.RHS[start.node])]*2
        self.x = self.model.nodes.x[start.node]
        self.y = self.model.nodes.y[start.node]
        self.start = start

    def create_top_node(self):
        top_node.ind = 0
        top_node = TopNode()
        top_node.node = self.model.robot.goal_node
        top_node.h_cost = cal_distance(self.model.robot.xs, self.model.robot.ys,
                                       self.model.robot.xt, self.model.robot.yt, self.model.dist_type)
        top_node.key = [self.h_cost, 0]

    def create_sol(self):
        sol = Sol()
        sol.nodes = self.path_nodes
        sol.x = [self.model.nodes.x[i] for i in self.path_nodes]
        sol.y = [self.model.nodes.y[i] for i in self.path_nodes]
        sol.dirs = self.node_to_dir(self.model, self.path_nodes)
        self.sol = Sol()

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
            dirs.append(theta)

        dirs.append(dirs[-1])
        return dirs

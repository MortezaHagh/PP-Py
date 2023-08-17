import time
import numpy as np
from common.cal_distance import cal_distance
from LPAStar.support import Open, Sol, TopNode


class LPAStar:
    def __init__(self, model):

        # stats
        self.n_closed = 0
        self.n_opened = 0
        self.n_reopened = 0
        self.n_expanded = 0
        self.n_final_open = 0

        # initialize
        self.model = model
        top_node = self.create_top_node()
        RHS = model.RHS
        RHS[top_node.node] = 0
        self.open = Open(top_node)
        self.G = model.G
        self.RHS = model.RHS

        # start
        self.current_dir = self.model.robot.dir
        self.path_nodes = [self.model.robot.start_node]

        # start process time
        self.end_time = 0
        start_time = time.process_time()

        # dstar_lite
        self.lpastar()

        # end process time
        self.sol.proc_time = self.end_time - start_time

    # ------------------------------------------------------------

    def lpastar(self):
        t = 1

        # # main procedure
        while self.model.start_node != self.model.robot.goal_node:
            # compute shortest path
            self.compute_shortest_path()

            #
            path_nodes = self.final_path_nodes()

            # move robot to next node
            self.model.start_node = path_nodes[1]
            self.path_nodes.append(path_nodes[1])
            t += 1

            # check for update in edge costs (obstacles)
            self.update_map(t)

        self.end_time = time.process_time()
        self.create_sol()
        self.n_final_open = len(self.open.list)

    # ------------------------------------------------------------

    def compute_shortest_path(self):

        # select top key
        self.top_key()

        # update goal_key
        goal_node = self.model.robot.goal_node
        c = min(self.G[goal_node], self.RHS[goal_node])
        goal_key = [c, c]

        while self.compare_keys(self.top_node.key, goal_key) or self.RHS[goal_node] != self.G[goal_node]:
            # remove topkey from open
            self.open.list.pop(self.top_node.ind)
            self.open.count = self.open.count - 1

            # update vertex
            update_list = self.model.successors[self.top_node.node]
            update_list = list(update_list)

            if self.G[self.top_node.node] > self.RHS[self.top_node.node]:
                self.G[self.top_node.node] = self.RHS[self.top_node.node]
            else:
                self.G[self.top_node.node] = np.inf
                update_list.append(self.top_node.node)
            self.update_vertex(update_list)

            # select top key
            self.top_key()

            # update goal_key
            c = min(self.G[goal_node], self.RHS[goal_node])
            goal_key = [c, c]

    # ------------------------------------------------------------

    def update_vertex(self, update_list):
        for inode in update_list:
            if inode != self.model.start_node:
                self.n_expanded += 1
                pred = self.model.predecessors[inode]
                pred_c = self.model.pred_cost[inode]
                pred_g = np.array(self.G[pred])
                self.RHS[inode] = min(pred_g+pred_c)

            open_nodes = [op.node for op in self.open.list]
            flag_reopen = False
            if inode in open_nodes:
                ind = open_nodes.index(inode)
                self.open.list.pop(ind)
                self.open.count -= 1
                flag_reopen = True

            if self.G[inode] != self.RHS[inode]:
                self.open.count += 1
                op = TopNode()
                op.node = inode
                x = self.model.nodes.x[inode]
                y = self.model.nodes.y[inode]
                h_cost = cal_distance(self.model.robot.xt, self.model.robot.yt, x, y, self.model.dist_type)
                c = min(self.G[inode], self.RHS[inode])
                op.key = [c + h_cost, c]
                op.ind = self.open.count
                self.open.list.append(op)
                self.n_opened += 1
                if flag_reopen:
                    self.n_reopened += 1

    def update_map(self, t):
        for i, do_t in enumerate(self.model.dynamic_obsts.t):
            if t == do_t:
                new_obst_node = self.model.dynamic_obsts.nodes[i]
                self.model.pred_cost[new_obst_node] = np.inf

                #  update vertex
                self.update_vertex([new_obst_node])

    def final_path_nodes(self):
        i = 0
        path_nodes = []
        node_number = self.model.robot.goal_node
        path_nodes.append(node_number)

        if self.model.expand_method == 'random':
            while node_number != self.model.start_node:
                i += 1
                preds = self.model.predecessors[node_number]
                pred_c = self.model.pred_cost[node_number]
                pred_g = np.array(self.G[preds])
                min_ind = np.argmin(pred_c+pred_g)
                node_number = preds[min_ind]
                path_nodes.append(node_number)
        elif self.model.expand_method == 'heading':
            while node_number != self.model.start_node:
                i += 1
                preds = self.model.predecessors[node_number]
                pred_c = self.model.pred_cost[node_number]
                pred_g = np.array(self.G[preds])
                if i == 2:
                    min_ind = np.argmin(pred_c+pred_g)
                    node_number = preds[min_ind]
                    x1 = self.model.robot.xt
                    y1 = self.model.robot.yt
                    x2 = self.model.nodes.x[node_number]
                    y2 = self.model.nodes.y[node_number]
                    current_dir = np.arctan2(y2-y1, x2-x1)
                elif i > 2:
                    dtheta = self.turn_cost(preds, node_number, current_dir)
                    c1 = pred_c+pred_g
                    c2 = [np.abs(dtheta), c1]
                    c3 = np.array(c2)
                    inds = np.lexsort(c3)
                    node_number = preds[inds[0]]
                    current_dir = current_dir + dtheta[inds[0]]
                path_nodes.append(node_number)

        path_nodes.reverse()
        return path_nodes

    # ------------------------------------------------------------

    def top_key(self):
        keys = np.array([[np.random.rand(1)[-1], op.key[1], op.key[0]]
                        for op in self.open.list])
        ind = np.lexsort(keys.T)
        top_node = self.open.list[ind[0]]
        top_node.ind = ind[0]
        self.top_node = top_node

    def turn_cost(self, preds, node, current_dir):
        dtheta = []
        y = self.model.nodes.y[node]
        x = self.model.nodes.x[node]
        for i in preds:
            dy = self.model.nodes.y[i]-y
            dx = self.model.nodes.x[i]-x
            theta = np.arctan2(dy, dx)
            dt = np.arctan2(np.sin(theta-current_dir), np.cos(theta-current_dir))
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

    # ------------------------------------------------------------

    def create_top_node(self):
        top_node = TopNode()
        top_node.ind = 0
        top_node.node = self.model.robot.start_node
        top_node.h_cost = cal_distance(self.model.robot.xs, self.model.robot.ys,
                                       self.model.robot.xt, self.model.robot.yt, self.model.dist_type)
        top_node.key = [top_node.h_cost, 0]
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

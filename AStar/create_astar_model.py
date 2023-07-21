import numpy as np
from support import Neighbor
import matplotlib.pyplot as plt
from common.create_model_base import CreateBaseModel


class CreateAStarModel(CreateBaseModel):
    def __init__(self, setting, has_dynamic_obsts=False, use_rnd=False):
        CreateBaseModel.__init__(self, has_dynamic_obsts, use_rnd)
        print('Create A* Model from Base Model')

        # settings
        if setting['adj_type'] == '4adj':
            ixy = [[1, 0], [0, 1], [0, -1], [-1, 0]]
            nAdj = 4
        elif setting['adj_type'] == '8adj':
            ixy = [[1, 0], [0, 1], [0, -1], [-1, 0],
                   [1, 1], [-1, -1], [-1, 1], [1, -1]]
            nAdj = 8

        if setting['dist_type'] == 'manhattan':
            edge_len = 2
        elif setting['dist_type'] == 'euclidean':
            edge_len = np.sqrt(2)

        self.adj_type = setting['adj_type']
        self.dist_type = setting['dist_type']
        self.expand_method = setting['expand_method']

        # neighbors
        neighbors = [[] for i in range(self.nodes.count)]

        for inode in range(self.nodes.count):
            if not inode in self.obsts.nodes:
                xnode = self.nodes.x[inode]
                ynode = self.nodes.y[inode]

                for iadj in range(nAdj):
                    ix = ixy[iadj][0]
                    iy = ixy[iadj][1]
                    newx = xnode+ix
                    newy = ynode+iy
                    new_dir = np.arctan2(iy, ix)

                    # check if the Node is within array bound
                    if (self.map.x_min <= newx <= self.map.x_max) and (self.map.y_min <= newy <= self.map.y_max):
                        new_node = inode+ix+iy*(self.map.nx)

                        if not new_node in self.obsts.nodes:

                            if ix != 0 and iy != 0:
                                cost = edge_len
                            else:
                                cost = 1

                            new_neighb = Neighbor()
                            new_neighb.x = newx
                            new_neighb.y = newy
                            new_neighb.cost = cost
                            new_neighb.dir = new_dir
                            new_neighb.node = new_node
                            neighbors[inode].append(new_neighb)

        self.neighbors = neighbors

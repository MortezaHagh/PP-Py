import math
import numpy as np
import matplotlib.pyplot as plt


class Map(object):
    def __init__(self):
        lim = 26
        self.lim = lim
        self.x_min = 0
        self.y_min = 0
        self.x_max = lim
        self.y_max = lim
        self.nx = self.x_max - self.x_min + 1
        self.ny = self.y_max - self.y_min + 1


class Robot(object):
    def __init__(self, map, use_rnd=False):
        dist = 0
        if use_rnd:
            lx = map.x_max - map.x_min
            ly = map.y_max - map.y_min
            l = np.sqrt(lx * lx + ly * ly)/1.5
            while dist < l:
                xx = np.random.randint(map.x_min, map.x_max, size=2)
                yy = np.random.randint(map.y_min, map.y_max, size=2)
                dist = np.sqrt((xx[0]-xx[1])**2 + (yy[0]-yy[1])**2)
            self.xs = xx[0]
            self.ys = yy[0]
            self.xt = xx[1]
            self.yt = yy[1]
            self.dir = math.pi/2
            self.goal_node = (self.yt - map.y_min)*(map.nx) + self.xt-map.x_min
            self.start_node = (self.ys - map.y_min)*(map.nx) + self.xs-map.x_min
        else:
            self.xs = 1
            self.ys = 1
            self.xt = 7
            self.yt = 7
            self.dir = math.pi/2
            self.goal_node = (self.yt - map.y_min)*(map.nx) + self.xt-map.x_min
            self.start_node = (self.ys - map.y_min) * \
                (map.nx) + self.xs-map.x_min


class Obstacles(object):
    def __init__(self, map, nodes=False, robot=None, use_rnd=False):
        self.map = map
        self.nodes = nodes
        self.robot = robot

        self.r = 0.25
        if use_rnd:
            self.random_obstacles()
        else:
            self.obstacles1()
        self.count = len(self.x)

    def obstacles1(self):
        xc1 = [3, 3, 3, 5, 5, 5, 7, 7, 7, 9, 9, 9, 11, 11, 11]
        yc1 = [3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5]
        xc2 = xc1*4
        yc2 = yc1 + [y+6 for y in yc1] + \
            [y+11 for y in yc1] + [y+16 for y in yc1]
        xc3 = [x+12 for x in xc2]
        yc3 = yc2
        self.x = xc2 + xc3
        self.y = yc2 + yc3
        self.nodes = [(y-self.map.y_min)*self.map.nx + x -
                      self.map.x_min for x, y in zip(self.x, self.y)]

    def random_obstacles(self):
        i = 0
        n = 400
        x, y, nodes = np.zeros(n), np.zeros(n), np.zeros(n)
        while i < n:
            xo = np.random.randint(self.map.x_min, self.map.x_max, 1)
            yo = np.random.randint(self.map.y_min, self.map.y_max, 1)
            node = (yo-self.map.y_min)*self.map.nx + xo - self.map.x_min
            node = int(node)
            if node not in [self.robot.start_node, self.robot.goal_node]:
                x[i] = self.nodes.x[node]
                y[i] = self.nodes.y[node]
                nodes[i] = node
                i += 1
        self.x = x
        self.y = y
        self.nodes = nodes


class DynamicObsts:
    def __init__(self, map, has_dynamic_obsts=False):
        if has_dynamic_obsts:
            self.t = [2, 4]
            self.x = [3, 7]
            self.y = [2, 2]
            self.nodes = [(y-map.y_min)*map.nx + x -
                          map.x_min for x, y in zip(self.x, self.y)]
        else:
            self.t = []
            self.x = []
            self.y = []
            self.nodes = []


class Nodes(object):
    def __init__(self, map):
        self.count = map.nx*map.ny
        self.x = [x for x in range(map.x_min, map.x_max+1)]*map.ny
        self.y = [y for y in range(map.y_min, map.y_max+1)
                  for x in range(map.nx)]


class CreateBaseModel(object):
    def __init__(self, has_dynamic_obsts=False, use_rnd=False):
        print('Create Base Model')

        # Map
        map = Map()
        self.map = Map()

        # Nodes
        self.nodes = Nodes(map)

        # Robot
        self.robot = Robot(map, use_rnd)

        # Obstacles
        self.obsts = Obstacles(map, self.nodes, self.robot, use_rnd)

        # Dynamic Obstacles
        self.dynamic_obsts = DynamicObsts(map, has_dynamic_obsts)

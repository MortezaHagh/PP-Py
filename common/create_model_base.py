from common.model_inputs import ModelInputs


class StartGoal:
    def __init__(self, x, y, node, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.node = node


class Map(object):
    def __init__(self, inputs):
        self.lim = inputs.lim
        self.x_min = inputs.x_min
        self.y_min = inputs.y_min
        self.x_max = inputs.x_max
        self.y_max = inputs.y_max
        self.nx = self.x_max - self.x_min + 1
        self.ny = self.y_max - self.y_min + 1


class Robot(object):
    def __init__(self, map, inputs):
        self.xs = inputs.xs
        self.ys = inputs.ys
        self.xt = inputs.xt
        self.yt = inputs.yt
        self.dir = inputs.heading
        self.goal_node = (self.yt - map.y_min)*(map.nx) + self.xt-map.x_min
        self.start_node = (self.ys - map.y_min) * \
            (map.nx) + self.xs-map.x_min


class Obstacles(object):
    def __init__(self, map, inputs):
        self.r = 0.25
        self.x = inputs.x_obst
        self.y = inputs.y_obst
        self.count = len(self.x)
        self.nodes = [(y-map.y_min)*map.nx + x -
                      map.x_min for x, y in zip(self.x, self.y)]


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
    def __init__(self, has_dynamic_obsts=False, use_rnd=False, map_id=1):
        print('Create Base Model')

        # model inputs
        inp = ModelInputs(map_id=map_id)

        # Map
        map = Map(inp)
        self.map = map

        # Nodes
        self.nodes = Nodes(map)

        # Robot
        robot = Robot(map, inp)
        self.robot = robot

        # Obstacles
        self.obsts = Obstacles(map, inp)

        # Dynamic Obstacles
        self.dynamic_obsts = DynamicObsts(map, has_dynamic_obsts)

        # start - goal
        self.start = StartGoal(robot.xs, robot.ys, robot.start_node, robot.dir)
        self.goal = StartGoal(robot.xt, robot.yt, robot.goal_node, robot.dir)

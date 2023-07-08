import os
import sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

import time
import matplotlib.pyplot as plt
from dstar_lite import dstar_lite
from common.cal_cost import cal_cost
from common.plot_model import plot_model
from common.plot_solution import plot_solution
from common.plot_animation import PlotAnimation1
from common.cal_smoothness import cal_smoothness
from create_dstarlite_model import CreateDstarLiteModel

# adj_type: 4adj or 8adj
# expand_method: random or heading
# dist_type: manhattan or euclidean
setting = {'adj_type': '4adj', 
           'dist_type': 'manhattan',
           'expand_method': 'heading'}

# model
model = CreateDstarLiteModel(setting)

# process time
t_start = time.process_time()

# dstar lite
[model, path] = dstar_lite(model)
path_time = time.process_time()-t_start

# cost and smoothness
path_length = cal_cost(path)
path_smoothness = cal_smoothness(path)
path_turns = path_smoothness/90

# results
print('nodes:', path.nodes)
print('dirs:', path.dirs)
print('turns:', path_turns, ' |||  time:', path_time)
print('length:', path_length, ' |||  smoothness:', path_smoothness) 

# plot
fig, ax = plot_model(model)
plot_solution(path, ax)
plt.show()

# # animation
# fig, ax = plot_model(model)
# animation = PlotAnimation1(fig, ax, path)
# animation.anim.save('results/animation1.gif', fps=4)
# plt.show()

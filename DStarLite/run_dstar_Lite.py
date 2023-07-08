import os
import sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

import time
import matplotlib.pyplot as plt
from dstar_lite import DStarLite
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

# dstar lite
dl_obj = DStarLite(model)

# cost and smoothness
path_length = cal_cost(dl_obj.sol)
path_smoothness = cal_smoothness(dl_obj.sol)
path_turns = path_smoothness/90

# results
print('nodes:', dl_obj.sol.nodes)
print('dirs:', dl_obj.sol.dirs)
print('turns:', path_turns, ' |||  time:', dl_obj.sol.proc_time)
print('length:', path_length, ' |||  smoothness:', path_smoothness) 

# plot
fig, ax = plot_model(model)
plot_solution(dl_obj.sol, ax)
plt.show()

# # animation
# fig, ax = plot_model(model)
# animation = PlotAnimation1(fig, ax, path)
# animation.anim.save('results/animation1.gif', fps=4)
# plt.show()

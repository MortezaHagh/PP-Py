import os
import sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

import matplotlib.pyplot as plt
from dstar_lite import DStarLite
from common.plotting import Plotter
from common.evaluate import Evaluate
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
dsl_obj = DStarLite(model)

# Evaluate
eval = Evaluate(dsl_obj.sol)

# results
print('nodes:', dsl_obj.sol.nodes)
print('dirs:', dsl_obj.sol.dirs)
print('turns:', eval.path_turns, ' |||  time:', dsl_obj.sol.proc_time)
print('length:', eval.path_length, ' |||  smoothness:', eval.smoothness) 

# plot
plotter = Plotter(model)
plotter.plot_solution(dsl_obj.sol)
plt.show()

# # animation
# fig, ax = plot_model(model)
# animation = PlotAnimation1(fig, ax, path)
# animation.anim.save('results/animation1.gif', fps=4)
# plt.show()

import os
import sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

from astar import AStar
import matplotlib.pyplot as plt
from common.plotting import Plotter
from common.evaluate import Evaluate
from create_astar_model import CreateAStarModel

# adj_type: 4adj or 8adj
# expand_method: random or heading
# dist_type: manhattan or euclidean
setting = {'adj_type': '4adj', 
           'dist_type': 'manhattan',
           'expand_method': 'random'}

# model
model = CreateAStarModel(setting, has_dynamic_obsts=False, use_rnd=False)

# dstar lite
astar_obj = AStar(model)

# Evaluate
eval = Evaluate(astar_obj.sol)
astar_obj.sol.proc_time = round(astar_obj.sol.proc_time, 4)

# results
print('nodes:', astar_obj.sol.nodes)
print('dirs:', astar_obj.sol.dirs)
print('turns:', eval.path_turns, '      |||  time:', astar_obj.sol.proc_time)
print('length:', eval.path_length, '    |||  smoothness:', eval.smoothness) 

# plot
plot_dyno = False # False True
plotter = Plotter(model, plot_dyno)
plotter.plot_solution(astar_obj.sol)
plt.show()

# # animation
# plot_dyno = False # False True
# plotter = Plotter(model, plot_dyno)
# plotter.plot_anim(astar_obj.sol)
# plotter.anim.save('sim-1.gif', fps=4)
# plt.show()

import os
import sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

import matplotlib.pyplot as plt
from lpastar import LPAStar
from common.plotting import Plotter
from common.evaluate import Evaluate
from create_lpastar_model import CreateLPAStarModel

# adj_type: 4adj or 8adj
# expand_method: random or heading
# dist_type: manhattan or euclidean
setting = {'adj_type': '8adj', 
           'dist_type': 'euclidean',
           'expand_method': 'heading'}

# model
model = CreateLPAStarModel(setting, has_dynamic_obsts=True, use_rnd=False)

# dstar lite
lpas_obj = LPAStar(model)

# Evaluate
eval = Evaluate(lpas_obj.sol)
lpas_obj.sol.proc_time = round(lpas_obj.sol.proc_time, 3)

# results
print('nodes:', lpas_obj.sol.nodes)
print('dirs:', lpas_obj.sol.dirs)
print('turns:', eval.path_turns, '      |||  time:', lpas_obj.sol.proc_time)
print('length:', eval.path_length, '    |||  smoothness:', eval.smoothness) 

# plot
plot_dyno = True # False True
plotter = Plotter(model, plot_dyno)
plotter.plot_solution(lpas_obj.sol)
plt.show()

# # animation
# plot_dyno = False # False True
# plotter = Plotter(model, plot_dyno)
# plotter.plot_anim(lpas_obj.sol)
# plotter.anim.save('sim-1.gif', fps=4)
# plt.show()

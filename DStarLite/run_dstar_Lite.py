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
setting = {'adj_type': '8adj', 
           'dist_type': 'euclidean',
           'expand_method': 'heading'}

# model
model = CreateDstarLiteModel(setting, has_dynamic_obsts=True, use_rnd=False)

# dstar lite
dsl_obj = DStarLite(model)

# Evaluate
eval = Evaluate(dsl_obj.sol)
dsl_obj.sol.proc_time = round(dsl_obj.sol.proc_time, 3)

# results
print(' ----------- results ------------')
print('nodes:', dsl_obj.sol.nodes)
print('dirs:', dsl_obj.sol.dirs)
print('time:', dsl_obj.sol.proc_time)
print('length:', eval.path_length)
print('turns:', eval.path_turns)
print('smoothness:', eval.smoothness)
print(' --------------------------------')
# print('n_expanded:', dsl_obj.n_expanded)
# print('n_opened:', dsl_obj.n_opened)
# print('n_reopened:', dsl_obj.n_reopened)
# print('n_final_open:', dsl_obj.open.count)


# plot
name = 'sim-2'
do_animate = False  # True - False
if not do_animate:
    plot_dyno = True
    plotter = Plotter(model, plot_dyno)
    name = name + '.png'
    pic_name = os.path.join(script_directory, 'Results/'+name) 
    plotter.plot_solution(dsl_obj.sol)
    plotter.fig.savefig(pic_name)
else:
    plot_dyno = False
    plotter = Plotter(model, plot_dyno)
    name = name + '.gif'
    pic_name = os.path.join(script_directory, 'Results/'+name) 
    plotter.plot_anim(dsl_obj.sol)
    plotter.anim.save(pic_name, fps=4)
plt.show()
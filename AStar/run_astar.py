import os
import sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

# astar - astar_heap
from astar_heap import AStar
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
model = CreateAStarModel(setting, has_dynamic_obsts=False, use_rnd=False, map_id=1)


# A* --------------------------------
astar_obj = AStar(model)
# -----------------------------------


# Evaluate
eval = Evaluate(astar_obj.sol)
astar_obj.sol.proc_time = round(astar_obj.sol.proc_time, 4)

# results
print(' ----------- results ------------')
print('nodes:', astar_obj.sol.nodes)
print('dirs:', astar_obj.sol.dirs)
print('time:', astar_obj.sol.proc_time)
print('length:', eval.path_length)
print('turns:', eval.path_turns)
print('smoothness:', eval.smoothness)
print(' ---------- statistics ---------')
print('n_expanded:', astar_obj.n_expanded)
print('n_opened:', astar_obj.n_opened)
print('n_reopened:', astar_obj.n_reopened)
print('n_final_open:', astar_obj.n_final_open)
print('n_closed:', astar_obj.n_closed)


# plot
name = 'sim-2'
plot_dyno = False
do_animate = False  # True - False
plotter = Plotter(model, plot_dyno)
if not do_animate:
    name = name + '.png'
    pic_name = os.path.join(script_directory, 'Results/'+name) 
    plotter.plot_solution(astar_obj.sol)
    # plotter.fig.savefig(pic_name)
else:
    name = name + '.gif'
    pic_name = os.path.join(script_directory, 'Results/'+name) 
    plotter.plot_anim(astar_obj.sol)
    plotter.anim.save(pic_name, fps=4)
plt.show()

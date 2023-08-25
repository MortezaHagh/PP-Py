import os
import sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

# astar - astar_heap
from AStar.astar_heap import AStar
from common.evaluate import Evaluate
from common.result import save_plot_result
from AStar.create_astar_model import CreateAStarModel

# adj_type: 4adj or 8adj
# expand_method: random or heading
# dist_type: manhattan or euclidean
method = "AStar"
map_id = 1
setting = {'adj_type': '4adj', 
           'dist_type': 'manhattan',
           'expand_method': 'random'}
settings_data = {"method": method, "do_plot": False, "do_save":True, "plot_dyno": False, "plot_anim": False, "map_id": map_id}

# model
model = CreateAStarModel(setting, has_dynamic_obsts=False, use_rnd=False, map_id=map_id)


# A* --------------------------------
pp_obj = AStar(model)
# -----------------------------------


# Evaluate
pp_obj.sol.proc_time = round(pp_obj.sol.proc_time, 4)
eval = Evaluate(pp_obj, method)

# results - save and plot
save_plot_result(model, pp_obj, eval, settings_data)
import os
import sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

# peastar - peaastar_heap
from common.evaluate import Evaluate
from PEAStar.peastar import PEAStar
from common.result import save_plot_result
from PEAStar.create_astar_model import CreateAStarModel

# adj_type: 4adj or 8adj
# expand_method: random or heading
# dist_type: manhattan or euclidean
method = "PEAStar"
map_id = 1
setting = {'adj_type': '4adj', 
           'dist_type': 'manhattan',
           'expand_method': 'random'}
settings_data = {"method": method, "do_plot": False, "plot_dyno": False, "plot_anim": False, "map_id": map_id}


# model
model = CreateAStarModel(setting, has_dynamic_obsts=False, use_rnd=False, map_id=map_id)


# PEA*
pp_obj = PEAStar(model)
# ---------------------------


# Evaluate
pp_obj.sol.proc_time = round(pp_obj.sol.proc_time, 4)
eval = Evaluate(pp_obj, method)

# results - save and plot
save_plot_result(model, pp_obj, eval, settings_data)
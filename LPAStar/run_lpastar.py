import os
import sys
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

from common.evaluate import Evaluate
from LPAStar.lpastar import LPAStar
from common.result import save_plot_result
from LPAStar.create_lpastar_model import CreateLPAStarModel

# adj_type: 4adj or 8adj
# expand_method: random or heading
# dist_type: manhattan or euclidean
method = "LPAStar"
map_id = 1
setting = {'adj_type': '8adj', 
           'dist_type': 'euclidean',
           'expand_method': 'heading'}
settings_data = {"method": method, "do_plot": False, "plot_dyno": False, "plot_anim": False, "map_id": map_id}

# model
model = CreateLPAStarModel(setting, has_dynamic_obsts=True, use_rnd=False, map_id=map_id)


# LPA*
pp_obj = LPAStar(model)
# ------------------------------------


# Evaluate
pp_obj.sol.proc_time = round(pp_obj.sol.proc_time, 3)
eval = Evaluate(pp_obj, method)

# results - save and plot
save_plot_result(model, pp_obj, eval, settings_data)
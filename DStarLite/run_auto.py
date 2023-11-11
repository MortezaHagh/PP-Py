import os
import sys
import json

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

# astar - astar_heap
from DStarLite.dstar_lite import DStarLite
from common.evaluate import Evaluate
from common.save_plot_result import save_plot_result
from common.update_settings import update_settings
from DStarLite.create_dstarlite_model import CreateDstarLiteModel

# setting
auto = True
just_one = True
setting_pp, setting_model = update_settings(just_one, auto, "DStarLite", 4)

# ----------------------------------------------------------

# model
model = CreateDstarLiteModel(setting_model, has_dynamic_obsts=True, use_rnd=False, map_id=setting_pp["map_id"])


# PP
pp_obj = DStarLite(model)

# ----------------------------------------------------------

# Evaluate
pp_obj.sol.proc_time = round(pp_obj.sol.proc_time, 4)
eval = Evaluate(pp_obj, setting_pp)

# results - save and plot
save_plot_result(model, pp_obj, eval, setting_pp)
import os
import sys
import json

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

# astar - astar_heap
from PEAStar.peastar import PEAStar
from common.evaluate import Evaluate
from common.save_plot_result import save_plot_result
from common.update_settings import update_settings
from PEAStar.create_astar_model import CreateAStarModel

# setting
auto = True
just_one = True
setting_pp, setting_model = update_settings(just_one, auto, "PEAStar", 1)

# ----------------------------------------------------------

# model
model = CreateAStarModel(setting_model, has_dynamic_obsts=False, use_rnd=False, map_id=setting_pp["map_id"])


# PP
pp_obj = PEAStar(model)

# ----------------------------------------------------------

# Evaluate
pp_obj.sol.proc_time = round(pp_obj.sol.proc_time, 4)
eval = Evaluate(pp_obj, setting_pp)

# results - save and plot
save_plot_result(model, pp_obj, eval, setting_pp)
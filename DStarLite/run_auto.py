import os
import sys
import json

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

from common.evaluate import Evaluate
from DStarLite.dstar_lite import DStarLite
from common.result import save_plot_result
from DStarLite.create_dstarlite_model import CreateDstarLiteModel

# # settings ---------------------------------------------
setting_path = "/home/piotr/dev/MRPP/PathPlanningPy/settings.json"
with open(setting_path, 'r') as f:
    settings = json.load(f)

setting_result = settings["setting_result"]
setting_model = settings["setting_model"]
setting_result["method"] = "DStarLite"

# ---------------------------------------------------------

# model
model = CreateDstarLiteModel(setting_model, has_dynamic_obsts=True, use_rnd=False, map_id=setting_result["map_id"])


# dstar lite
pp_obj = DStarLite(model)
# -----------------------------------


# Evaluate
pp_obj.sol.proc_time = round(pp_obj.sol.proc_time, 3)
eval = Evaluate(pp_obj, setting_result["method"])

# results - save and plot
save_plot_result(model, pp_obj, eval, setting_result)

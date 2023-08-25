import os
import sys
import json

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.join(script_directory, '..'))

# astar - astar_heap
from AStar.astar_heap import AStar
from common.evaluate import Evaluate
from common.result import save_plot_result
from AStar.create_astar_model import CreateAStarModel

# # settings ---------------------------------------------
setting_path = "/home/piotr/dev/MRPP/PathPlanningPy/settings.json"
with open(setting_path, 'r') as f:
    settings = json.load(f)

setting_result = settings["setting_result"]
setting_model = settings["setting_model"]
setting_result["method"] = "Astar"

# ---------------------------------------------------------

# model
model = CreateAStarModel(setting_model, has_dynamic_obsts=False, use_rnd=False, map_id=setting_result["map_id"])


# A* --------------------------------
pp_obj = AStar(model)
# -----------------------------------


# Evaluate
pp_obj.sol.proc_time = round(pp_obj.sol.proc_time, 4)
eval = Evaluate(pp_obj, setting_result["method"])

# results - save and plot
save_plot_result(model, pp_obj, eval, setting_result)
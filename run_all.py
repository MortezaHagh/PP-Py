import os
import csv

# 
filename = "/home/piotr/dev/MRPP/PathPlanningPy/result.csv"
with open(filename, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["method", "max_steps", "path_length", "smoothness", "path_turns", "proc_time", "n_expanded", "n_opened", "n_reopened", "n_final_open"])

# 
path_AStar = "/home/piotr/dev/MRPP/PathPlanningPy/AStar/run_astar.py"
path_PEAStar = "/home/piotr/dev/MRPP/PathPlanningPy/PEAStar/run_peastar.py"
path_EPEAStar = "/home/piotr/dev/MRPP/PathPlanningPy/EPEAStar/run_epeastar.py"
path_LPAStar = "/home/piotr/dev/MRPP/PathPlanningPy/LPAStar/run_lpastar.py"
path_DStarLite = "/home/piotr/dev/MRPP/PathPlanningPy/DStarLite/run_dstar_Lite.py"

os.system("python3 " + path_AStar)
os.system("python3 " + path_PEAStar)
os.system("python3 " + path_EPEAStar)
os.system("python3 " + path_LPAStar)
os.system("python3 " + path_DStarLite)


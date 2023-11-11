import os
import csv
import sys

#
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
base_path = os.path.join(script_directory, '..')
# base_path = "/home/piotr/dev/MRPP/PathPlanningPy/"

Methods = ["AStar", "PEAStar", "EPEAStar", "LPAStar", "DStarLite"]
filename = os.path.join(base_path, "zResults/Auto/results_all.csv")
with open(filename, 'w+', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["method", "max_steps", "path_length", "smoothness", "path_turns",
                    "proc_time", "n_expanded", "n_opened", "n_reopened", "n_final_open"])

#
path_AStar = os.path.join(base_path, "AStar/run_auto.py")
path_PEAStar = os.path.join(base_path, "PEAStar/run_auto.py")
path_EPEAStar = os.path.join(base_path, "EPEAStar/run_auto.py")
path_LPAStar = os.path.join(base_path, "LPAStar/run_auto.py")
path_DStarLite = os.path.join(base_path, "DStarLite/run_auto.py")

os.system("python3 " + path_AStar)
os.system("python3 " + path_PEAStar)
os.system("python3 " + path_EPEAStar)
os.system("python3 " + path_LPAStar)
os.system("python3 " + path_DStarLite)

import os
import sys
import matplotlib.pyplot as plt
from common.plotting import Plotter

result_path = "/home/piotr/dev/MRPP/PathPlanningPy"

def save_plot_result(model, pp_obj, eval, settings):
    # plot
    name = "sim-" + settings["method"] + "-" + str(settings["map_id"])
    if settings["do_plot"]:
        plotter = Plotter(model, settings["plot_dyno"])
        if not settings["plot_anim"]:
            name = name + '.png'
            pic_name = os.path.join(result_path, 'zResults/'+name) 
            plotter.plot_solution(pp_obj.sol)
            if settings["do_save"]: plotter.fig.savefig(pic_name)
        else:
            name = name + '.gif'
            pic_name = os.path.join(result_path, 'zResults/'+name) 
            plotter.plot_anim(pp_obj.sol)
            plotter.anim.save(pic_name, fps=4)
        plt.show()

    # results
    print(settings["method"] + ' ===========================')
    print('nodes:', pp_obj.sol.nodes)
    print('dirs:', pp_obj.sol.dirs)
    print('time:', pp_obj.sol.proc_time)
    print('length:', eval.path_length)
    print('turns:', eval.path_turns)
    print('smoothness:', eval.smoothness)
    print(' ---------- statistics ---------')
    print('n_expanded:', eval.n_expanded)
    print('n_opened:', eval.n_opened)
    print('n_reopened:', eval.n_reopened)
    print('n_final_open:', eval.n_final_open)
    print('n_closed:', eval.n_closed)
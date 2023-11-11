import os
import sys
import matplotlib.pyplot as plt
from common.plotting import Plotter


def save_plot_result(model, pp_obj, eval, setting_pp):

    result_path = setting_pp["save_path"]
    map_id = str(setting_pp["map_id"])
    method_name = setting_pp["method_name"]
    name = "sim-" + method_name + "-" + map_id

    # plot
    save_dir = os.path.join(result_path, 'Figs/' + name)
    plot_dyno = setting_pp["plot_dyno"]
    if setting_pp["do_plot"]:
        plotter = Plotter(model, plot_dyno)
        if not setting_pp["plot_anim"]:
            # plot
            plotter.plot_solution(pp_obj.sol)
            if setting_pp["do_save"]:
                plotter.fig.savefig(save_dir+".png")
        else:
            # animation
            plotter.plot_anim(pp_obj.sol)
            plotter.anim.save(save_dir+'.gif', fps=4)
        plt.show()

    # results
    do_print = setting_pp["do_print"]
    if do_print:
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

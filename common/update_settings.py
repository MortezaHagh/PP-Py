import os
import json


def update_settings(just_one=True, auto="true", method_name=None, method_id=None, setting_path=None):

    setting_path = setting_path
    if not setting_path:
        setting_path = "/home/piotr/dev/MRPP/PathPlanningPy/zMethodHandler/Settings/"

    if just_one:
        if auto:
            setting_file = "settings_auto.json"
        else:
            setting_file = "settings_auto.json"
    else:
        setting_file = "settings_auto.json"

    setting_full_path = os.path.join(setting_path, setting_file)
    with open(setting_full_path, 'r') as f:
        settings = json.load(f)

    setting_pp = settings["setting_pp"]
    setting_model = settings["setting_model"]
    setting_pp["method_name"] = method_name
    setting_pp["method_id"] = method_id

    save_name = "results_all.csv"
    setting_pp["save_name"] = save_name

    # if just_one:
    #     if auto:
    #         save_name = "map" + str(setting_pp["map_id"]) + "_"
    #         save_name = save_name + setting_pp["method_name"] + ".csv"
    #         setting_pp["save_name"] = save_name

    #     else:
    #         save_name = "results_all.csv"
    #     setting_pp["save_name"] = save_name

    print(" ==========================" + setting_pp["method_name"] + "========================== ")

    return setting_pp, setting_model

n_scenario = 16

import os
import argparse
import pandas as pd
import yaml
import json
import shutil
from utils import prepare_input
from main_model import two_stage_model

parser = argparse.ArgumentParser()
parser.add_argument('--scenario_id', type=int, required=True, help="Norta scenario id")

args = parser.parse_args()
scenario_id = args.scenario_id

dir_name = 'norta_sm_' + str(n_scenario) + "_" + str(scenario_id) +'/'

with open(r'config.yaml') as file:
    model_params = yaml.load(file, Loader=yaml.FullLoader)

model_params["path_to_input"] = "16_Scenario/"
model_params["input1"], model_params["input2"] = prepare_input(model_params["path_to_input"])

for column_id in model_params["input1"].columns:
    if "max_flood_level" in column_id:
        model_params["input1"][column_id] = 0

norta_scenario = pd.read_csv("../scenarios/" + str(scenario_id) + "/" + "Final_Input1.csv", index_col="Unnamed: 0")
set_of_flooded_substations = norta_scenario.columns
meow_maps = list(norta_scenario.index)


model_params["path_to_output"] = "/work/07346/ashukla/ls6/Norta_Results/" + dir_name
if os.path.exists(model_params["path_to_output"]):
    shutil.rmtree(model_params["path_to_output"], ignore_errors=True)
os.mkdir(model_params["path_to_output"])

for row_id in range(model_params["input1"].shape[0]):
    substation_ = model_params["input1"].iloc[row_id,2]
    if str(substation_) in set_of_flooded_substations:
        busnum = model_params["input1"].index[row_id]
        model_params["input1"].loc[busnum,meow_maps] = list(norta_scenario[str(substation_)])

budget_vector = [0,20,40,60,80]
base_model = two_stage_model(model_params)

for budget in budget_vector:
    base_model.budget_ref.rhs = budget*1e6
    base_model.model.setParam("LogFile", model_params["path_to_output"] + str(budget) + "M")
    base_model.model.setParam("MIPGap", model_params["mip_gap"])
    base_model.model.setParam("TimeLimit", model_params["time_limit"])
    base_model.model.setParam("Method", model_params["solver_method"])
    base_model.model.optimize()
    base_model.model.write(model_params["path_to_output"] + str(budget) + "M_" + "solution.sol")    
    print("\n\n*********************************************")
    print("*********************************************\n\n")

with open(model_params["path_to_output"] + 'model_params.json', 'w') as fp:
    del model_params["input1"]
    del model_params["input2"]
    json.dump(model_params, fp)
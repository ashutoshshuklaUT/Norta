import time
import pickle
import os
import pandas as pd
from norta import *

##############################################################################
##############################################################################
########## input parameters 

##############################################################################
##############################################################################



def get_df_for_heuristic():
    df = pd.read_csv("/Users/ashutoshshukla/Desktop/Data/fixed_reduced_grid/192_Scenario/Final_Input1.csv")
    # directions = ["w", "wnw", "nw", "nnw", "n", "nne"]
    # categories = ["2", "3", "4", "5"]
    # forward_speeds = ["05", "10", "15", "25"]
    directions = ["w", "wnw", "nw", "nnw"]
    categories = ["5"]
    forward_speeds = ["05", "10", "15", "25"]
    lister = []
    for i in directions:
        for j in range(len(categories)):
            for k in range(len(forward_speeds)):
                lister.append("max_flood_level_" + i +"_" + categories[j] + "_" + forward_speeds[k])
    df = df[list(df.columns[0:9]) + lister]
    df_sub = df[["SubNum", "load"]].groupby("SubNum").sum()
    df_flood = df[["SubNum"] + lister]
    df_flood = df_flood.drop_duplicates().set_index("SubNum") # drop duplicates
    df_flood = df_flood.loc[(df_flood.sum(axis=1) != 0), :] # drop substations that are not flooded
    """df_sub has load demand for all the substations"""
    """df_flood has only flooded substations"""
    return df, df_sub, df_flood

if __name__ == '__main__':    
    start_time = time.time()
    df, df_sub, df_flood = get_df_for_heuristic()
    df_flood = df_flood.T
    data = df_flood.iloc[:,:].values
    print("Code running okay")
    norta_data = fit_NORTA(data, data.shape[0], data.shape[1], 
                           np.cov(data, rowvar=False), lambda_param=0.001, 
                           mc_samples=4E6, output_flag=1, n_proc=4)

    parent_folder = "output"
    new_directory = "proportional_change_flood_" + str(data.shape[1]) + "d"
    
    
    
    
    new_directory_path = os.path.join(parent_folder, new_directory)
    os.makedirs(new_directory_path, exist_ok=True)

    with open(new_directory_path + "/norta_object", 'wb') as file:
        pickle.dump(norta_data, file)
    pd.DataFrame(np.cov(data, rowvar=False)).to_csv( new_directory_path + "/target_covariance.csv")
    pd.DataFrame(data).corr().to_csv(new_directory_path + "/target_correlation.csv", index=None)
    df_flood.to_csv(new_directory_path + "/source_df.csv")
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print the elapsed time
    print(f"Time taken to run the script: {elapsed_time} seconds")
    print("Dimension of the problem is: ", data.shape[1])
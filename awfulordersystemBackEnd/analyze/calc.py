import paintGraph
import re
import os
import datetime
import numpy as np
import pandas as pd


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


# def standardization(data):
#     mu = np.mean(data, axis=0)
#     sigma = np.std(data, axis=0)
#     return (data - mu) / sigma


if __name__ == "__main__":
    pass_list = []
    # pass_list = ["1651939259730", "1651939432772", "1651939937452", "1651940189994"]
    root_path = "../data/"
    # get date and time
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    os.mkdir(now)
    now += "/"

    for folder in os.listdir(root_path):
        if re.match("\d+", folder):
            if folder in pass_list:
                continue
            print(folder)
            paintGraph.paint(root_path, folder, now)

    for files in os.listdir(now):
        if re.match("统计\w+\.xlsx", files):
            print(files)
            df = pd.read_excel(now + files, keep_default_na=False)
            # print(df)

            # # normalization
            # metrics = ["fixation_count", "duration", "fixation_rate", "first_fixation_on_aoi", "scan_path_accuracy",
            #            "edit_distance", "attention_switch", "convex_hull"]
            # print(df[df["Metrics"] == "edit_distance"])
            # for metric in metrics:
            #     all_values = []
            #     print(df[df["Metrics"] == metric])
            #     for v in df[df["Metrics"] == metric]["Exp"].values:
            #         if v == "" or v == -1:
            #             continue
            #         all_values.append(v)
            #     for v in df[df["Metrics"] == metric]["Standard"].values:
            #         if v == "" or v == -1:
            #             continue
            #         all_values.append(v)
            #     correspond_values = {}
            #     if len(all_values) == 0:
            #         continue
            #     all_values_norm = normalization(all_values)
            #     for i in range(len(all_values_norm)):
            #         correspond_values[all_values[i]] = all_values_norm[i]
            #     for v in df[df["Metrics"] == metric]["Exp"].values:
            #         if v == "" or v == -1:
            #             df.loc[df["Exp"] == v, "Exp"] = ""
            #             continue
            #         df.loc[df["Exp"] == v, "Exp"] = correspond_values[v]
            #     print(df[df["Metrics"] == metric])
            #     for v in df[df["Metrics"] == metric]["Standard"].values:
            #         if v == "" or v == -1:
            #             df.loc[df["Standard"] == v, "Standard"] = ""
            #             continue
            #         df.loc[df["Standard"] == v, "Standard"] = correspond_values[v]
            #     print(df[df["Metrics"] == metric])
            #
            # df.to_excel(now + "归一" + files)




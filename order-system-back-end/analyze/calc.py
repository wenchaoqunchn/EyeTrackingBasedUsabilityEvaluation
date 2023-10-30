import analyze.paintGraph
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


def calc():
    pass_list = ['1652456595952']
    root_path = "./data/"
    # get date and time
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    now = "./analyze/" + now
    os.mkdir(now)
    now+='/'

    for folder in os.listdir(root_path):
        if re.match("\d+", folder):
            if folder in pass_list:
                continue
            print(folder)
            analyze.paintGraph.paint(root_path, folder, now)

    for files in os.listdir(now):
        if re.match("统计\w+\.xlsx", files):
            print(files)
            df = pd.read_excel(now + files, keep_default_na=False)
            # print(df)
    return now

if __name__ == "__main__":
    pass_list = ['1652456595952']
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


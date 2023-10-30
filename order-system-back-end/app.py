import os
import subprocess
import json
import time

from flask import Flask, request
import win32gui, win32ui, win32con, win32api

import analyze.calc as c
import pandas as pd


def window_capture(filename):
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)


timestamp = 0

app = Flask(__name__)


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("new folder created: " + path)
    else:
        print("folder already exists: " + path)


@app.route('/get_data', methods=['POST'])
def predict():
    global timestamp
    if request.method == 'POST':
        response = request.get_json()
        # json_line = json.dumps(json.loads(response))
        json_line = json.dumps(response)
        # print(response)

        if timestamp != 0:
            # window_capture("data/" + str(timestamp) + "/pic/" + str(response['unix_timestamp']) + ".jpg")
            with open("data/" + str(timestamp) + "/components.txt", "a") as f:
                # f.write(str(response) + "\n")
                f.write(str(json_line) + "\n")
                # f.write(json_line + "\n")

            try:
                os.rename(
                    "data/" + str(timestamp) + "/pic/tmp.jpg",
                    "data/"
                    + str(timestamp)
                    + "/pic/"
                    + str(response['unix_timestamp'])
                    + ".jpg",
                )
            except Exception as e:
                pass
        return "backend get data"


@app.route('/get_screenshots', methods=['POST'])
def get_screenshots():
    try:
        time.sleep(0.5)
        window_capture("data/" + str(timestamp) + "/pic/tmp" + ".jpg")
    except Exception as e:
        pass
    return "backend get screenshots"


@app.route('/start_record', methods=['POST'])
def start_record():
    global timestamp
    if request.method == 'POST':
        response = request.get_json()
        print(response)
        timestamp = response['unix_timestamp']
        mkdir("data/" + str(timestamp))
        mkdir("data/" + str(timestamp) + "/pic")
        p = subprocess.Popen(
            os.path.dirname(__file__)
            + "/eyetrack/cs_sample_streams.exe data/"
            + str(timestamp)
            + "/eye-track",
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            shell=True,
            close_fds=True,
            start_new_session=True,
        )

        with open("data/" + str(timestamp) + "/BadDesigns.json", "w") as f:
            f.write(json.dumps(response))

        return "backend start record"


@app.route('/stop_record', methods=['POST'])
def stop_record():
    global timestamp
    os.system("taskkill /f /im cs_sample_streams.exe")
    timestamp = 0
    print("backend stop record")
    return "backend stop record"


@app.route('/get_scores')
def get_scores():
    def file_filter(f):
        if f[-5:] in ['.xlsx']:
            return True
        else:
            return False

    dir = c.calc()
    files = os.listdir(dir)

    files = list(filter(file_filter, files))

    score_dict = {}

    formulas = [
        lambda V: 0.3 * (V['FC'] + 0.01 * V['FD'] - V['FR'] + 0.01 * V['FFT'])
        + 0.7 * (-V['SPA'] + V['ED'] + V['AS'] + V['CA'])
        - 100,
        lambda V: 3 * (-V['FR']) + 7 * (-V['SPA'] + V['AS'] + V['ED']),
        lambda V: 0.3 * (V['FR'] + 0.01 * V['FFT'])
        + 0.7 * (-V['SPA'] + 3 * V['ED'] + 2 * V['AS'])
        - 31,
        lambda V: 0.3 * (V['FC'] + 0.1 * V['FD'])
        + 0.7 * (-V['SPA'] + V['AS'] + V['CA'])
        - 300,
        lambda V: 0.03 * (100 * V['FC'] + 0.1 * V['FD'])
        + 0.07 * (-100 * V['SPA'] + 30 * V['AS'])
        - 95,
        lambda V: 10 * V['FC'] + 0.1 * V['FR'] - 600,
    ]

    form = {
        'scores': {
            'accessibility': 80.5,
            'easeOfUse': 32.5,
            'consistency': 70,
            'accuracy': 60,
            'deviceEfficiency': 45.3,
            'robustness': 75,
        }
    }

    names = form['scores'].keys()

    for i, file in enumerate(files):
        excel = pd.read_excel(io=dir + file)
        metric = file[2:-5]

        keys = ['FC', 'FD', 'FR', 'FFT', 'SPA', 'ED', 'AS', 'CA']
        V = {k: v for k, v in zip(keys, excel['Standard'].tolist())}
        # V={'FC': 1, 'FD': 211, 'FR': 1, 'FFT': 211, 'SPA': 1, 'ED': 0, 'AS': 0, 'CA': 0}
        score_dict[names[i]] = formulas[i](V)
    return {'scores': score_dict}



if __name__ == '__main__':
    app.run()

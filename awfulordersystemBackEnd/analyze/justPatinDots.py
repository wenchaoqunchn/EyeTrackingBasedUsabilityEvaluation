import json
from PIL import Image, ImageDraw
from analyze.min_circle import make_circle
import pandas as pd

def draw_eye_track_on_image(image, eye_track_data):
    draw = ImageDraw.Draw(image)
    points = []
    for data in eye_track_data:
        if data["validity"] == "invalid":
            continue
        points.append((data["x"], data["y"]))
    color_step = int(255 / (len(points)))
    for i, point in enumerate(points):
        x, y = point
        # draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255 - i * color_step, 0, 0))
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255 - i * color_step, 0, 0))
    return image

file_path = "../data/1651849989421/"

time_shift = 400

components = []
eye_track = []
AOIs = {}

with open(file_path + "components.txt", "r") as f:
    for line in f:
        json_data = json.loads(line)
        components.append(json_data)

with open(file_path + "eye-track.txt", "r") as f:
    for line in f:
        json_data = json.loads(line)
        eye_track.append(json_data)

for i in range(len(components)):
    end = components[i]["unix_timestamp"]
    if i == 0:
        begin = 0
    else:
        begin = components[i - 1]["unix_timestamp"]

    # begin -= time_shift
    begin += time_shift
    end += time_shift

    # 找到路径时间内的眼动数据
    time_window_eye_track = []
    for eye_track_data in eye_track:
        if eye_track_data["timestamp_unix"] < begin:
            # print(eye_track_data["timestamp_unix"], "<", begin)
            continue
        elif eye_track_data["timestamp_unix"] > end:
            # print(eye_track_data["timestamp_unix"], ">", end)
            break
        else:
            time_window_eye_track.append(eye_track_data)

    # 画图
    try:
        im = Image.open(file_path + "pic/" + str(components[i]["unix_timestamp"]) + ".jpg")
        im = draw_eye_track_on_image(im, time_window_eye_track)
        im.save(file_path + "pic/" + str(components[i]["unix_timestamp"]) + "_track.jpg")
    except Exception as e:
        print(e)
        pass
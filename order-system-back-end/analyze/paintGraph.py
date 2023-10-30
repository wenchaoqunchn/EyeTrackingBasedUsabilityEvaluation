import json
from PIL import Image, ImageDraw
from analyze.min_circle import make_circle
import pandas as pd


def calc_convex_hull(eye_track_data):
    points = []
    for eye_track in eye_track_data:
        if eye_track['fixation']:
            points.append((eye_track['x'], eye_track['y']))
    # print(points)
    if len(points) < 1:
        return {'x': 0, 'y': 0, 'radius': -1}
    x, y, r = make_circle(points)
    return {'x': x, 'y': y, 'radius': r}


def merge_multiple_fixations_to_one(eye_track_data):
    eye_track_data_short = []
    tmp_data = []
    for data in eye_track_data:
        if data["fixation"]:
            tmp_data.append(data)
        else:
            if len(tmp_data) > 0:
                points = []
                for data_ in tmp_data:
                    points.append((data_["x"], data_["y"]))
                x, y, r = make_circle(points)
                tmp = {
                    "x": x,
                    "y": y,
                    "radius": r,
                    "fixation": True,
                    "validity": "valid",
                    "timestamp_unix": tmp_data[0]["timestamp_unix"],
                    "duration": tmp_data[-1]["timestamp_unix"]
                    - tmp_data[0]["timestamp_unix"],
                }
                if tmp["duration"] != 0:
                    eye_track_data_short.append(tmp)
            tmp_data = []
            eye_track_data_short.append(data)
    return eye_track_data_short


def checkOverlap(
    self, radius: int, x_center: int, y_center: int, x1: int, y1: int, x2: int, y2: int
) -> bool:
    # x1 < x2 , y1 < y2
    dx = x1 - x_center if x1 > x_center else x_center - x2 if x_center > x2 else 0
    dy = y1 - y_center if y1 > y_center else y_center - y2 if y_center > y2 else 0
    return dx * dx + dy * dy <= radius * radius


def is_fixation_circle_overlap_AOI(AOI_size, fixayion_circle, border_size):
    x_min, x_max, y_min, y_max = AOI_size
    x, y, r = fixayion_circle
    r += border_size
    dx = x_min - x if x_min > x else x - x_max if x > x_max else 0
    dy = y_min - y if y_min > y else y - y_max if y > y_max else 0
    return dx * dx + dy * dy <= r * r


def mark_fixation_and_saccade(eye_track_data):
    # 打印eye_track_data两两之间的时间之差
    eye_track_data[0]['fixation'] = False
    for i in range(1, len(eye_track_data)):
        eye_track_data[i]['fixation'] = False
        if (
            eye_track_data[i]["validity"] == "invalid"
            or eye_track_data[i - 1]["validity"] == "invalid"
        ):
            continue
        x, y = eye_track_data[i]['x'], eye_track_data[i]['y']
        x_last, y_last = eye_track_data[i - 1]['x'], eye_track_data[i - 1]['y']
        distance = ((x - x_last) ** 2 + (y - y_last) ** 2) ** 0.5
        time = (
            eye_track_data[i]['timestamp_unix']
            - eye_track_data[i - 1]['timestamp_unix']
        )
        if time == 0:
            time = 0.00001
        speed = distance / time
        # print(speed)
        if speed < 0.3:
            eye_track_data[i]['fixation'] = True
    return eye_track_data


def draw_eye_track_on_image_no_fixation(image, eye_track_data):
    draw = ImageDraw.Draw(image)
    points = []
    for data in eye_track_data:
        if data["validity"] == "invalid":
            continue
        points.append((data["x"], data["y"]))
        # # point = (data['x'], data['y'])
        # x, y = data['x'], data['y']
        # # print(point)
        # draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 0, 0))
    color_step = int(255 / (len(points)))
    for i, point in enumerate(points):
        x, y = point
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255 - i * color_step, 0, 0))
    return image


def draw_eye_track_on_image(image, eye_track_data):
    draw = ImageDraw.Draw(image)
    points = []
    for data in eye_track_data:
        if data["validity"] == "invalid":
            continue
        points.append((data["x"], data["y"], data["fixation"]))
    color_step = int(255 / (len(points)))
    for i, point in enumerate(points):
        x, y, fixation = point
        # draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255 - i * color_step, 0, 0))
        if fixation:
            draw.ellipse(
                (x - 20, y - 20, x + 20, y + 20), fill=(255 - i * color_step, 0, 0)
            )
        else:
            draw.ellipse(
                (x - 5, y - 5, x + 5, y + 5), fill=(255 - i * color_step, 0, 0)
            )
    return image


def draw_eye_track_on_image_with_merged_fixation(image, eye_track_data):
    draw = ImageDraw.Draw(image)
    points = []
    for data in eye_track_data:
        if data["validity"] == "invalid":
            continue
        points.append(data)
    color_step = int(255 / (len(points)))
    for i, point in enumerate(points):
        # x, y, fixation = point["x"], point["y"], point["fixation"]
        # draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255 - i * color_step, 0, 0))
        if point["fixation"]:
            # print(point)
            draw.ellipse(
                (
                    point["x"] - point["radius"],
                    point["y"] - point["radius"],
                    point["x"] + point["radius"],
                    point["y"] + point["radius"],
                ),
                fill=(0, 255 - i * color_step, 0),
            )
            # draw.rectangle(((200, 200), (250, 250)), fill=None, outline=(0, 0, 255), width=5)
            draw.rectangle(
                (
                    (point["x"] - 10, point["y"] - 10),
                    (point["x"] + 10, point["y"] + 10),
                ),
                fill=None,
                outline=(0, 0, 255),
                width=5,
            )
        else:
            draw.ellipse(
                (point["x"] - 5, point["y"] - 5, point["x"] + 5, point["y"] + 5),
                fill=(255 - i * color_step, 0, 0),
            )
    return image


def draw_AOIs_on_image(im, AOIs_size):
    draw = ImageDraw.Draw(im)
    for aoi in AOIs_size:
        x_1, y_1, x_2, y_2 = aoi["x1"], aoi["y1"], aoi["x2"], aoi["y2"]
        draw.rectangle((x_1, y_1, x_2, y_2), outline=(0, 0, 255), width=2)
    return im


def count_and_duration_fixation_overlap_aoi(AOIs_size, eye_track_data):
    first_fixation_time = -1
    total_fixation_duration = 0
    total_fixation_count = 0
    fixation_on_aoi = 0
    sum_duration = 0
    for i, data in enumerate(eye_track_data):
        if not data["fixation"]:
            continue
        total_fixation_count += 1
        total_fixation_duration += data["duration"]
        x, y, r = data["x"], data["y"], data["radius"]
        data["aoi"] = ""
        for aoi in AOIs_size:
            # print("x:{}, y:{}, r:{}, ({}), ({}), {}".format(x, y, r, (aoi["x1"], aoi["y1"]), (aoi["x2"], aoi["y2"]), is_fixation_circle_overlap_AOI((aoi["x1"], aoi["x2"], aoi["y1"], aoi["y2"]), (x, y, r), 0)))
            if is_fixation_circle_overlap_AOI(
                (aoi["x1"], aoi["x2"], aoi["y1"], aoi["y2"]), (x, y, r), 0
            ):
                data["aoi"] = aoi["name"]
                fixation_on_aoi += 1
                sum_duration += data["duration"]
                if first_fixation_time == -1:
                    first_fixation_time = total_fixation_duration
                    break

    fixation_rate = (
        0 if total_fixation_count == 0 else fixation_on_aoi / total_fixation_count
    )
    return fixation_on_aoi, sum_duration, fixation_rate, first_fixation_time


def get_scanPath(eye_track_data, not_relevant_aois):
    scanPath = []
    for i, data in enumerate(eye_track_data):
        if not data["fixation"]:
            continue
        if data["aoi"] != "":
            scanPath.append({"aoi": data["aoi"], "relevant": True})
        else:
            for aoi in not_relevant_aois:
                if is_fixation_circle_overlap_AOI(
                    (aoi["x1"], aoi["x2"], aoi["y1"], aoi["y2"]),
                    (data["x"], data["y"], data["radius"]),
                    0,
                ):
                    data["aoi"] = aoi["name"]
                    scanPath.append({"aoi": data["aoi"], "relvant": False})
                    break
    return scanPath


def calc_scan_path_accuracy(scanPath, AOIs_id):
    visited_aois = []
    visited_not_relvant_aois = []
    all_aois = []
    for i, data in enumerate(scanPath):
        all_aois.append(data["aoi"])
        if data["aoi"] != "" and data["aoi"] in AOIs_id:
            visited_aois.append(data["aoi"])
        elif data["aoi"] != "" and data["aoi"] not in AOIs_id:
            visited_not_relvant_aois.append(data["aoi"])
    visited_aois = list(set(visited_aois))
    visited_not_relvant_aois = list(set(visited_not_relvant_aois))
    all_aois = list(set(all_aois))
    return len(visited_aois) / len(all_aois) if len(all_aois) != 0 else 0


def calc_attention_switch(scanPath):
    attention_switch = 0
    last_aoi = ""
    for i, data in enumerate(scanPath):
        if data["aoi"] == "":
            continue
        if last_aoi == "":
            last_aoi = data["aoi"]
        elif last_aoi != data["aoi"]:
            attention_switch += 1
            last_aoi = data["aoi"]
    return attention_switch


def minDistance(word1, word2) -> int:
    n1 = len(word1)
    n2 = len(word2)
    dp = [[0] * (n2 + 1) for _ in range(n1 + 1)]
    # 第一行
    for j in range(1, n2 + 1):
        dp[0][j] = dp[0][j - 1] + 1
    # 第一列
    for i in range(1, n1 + 1):
        dp[i][0] = dp[i - 1][0] + 1
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1]) + 1
    # print(dp)
    return dp[-1][-1]


def calc_edit_distance(scanPath, standard_scan_path):
    path = []
    standard_path = []
    for p in scanPath:
        if p["aoi"] != "":
            path.append(p["aoi"])
    for p in standard_scan_path:
        standard_path.append(p)
    return minDistance(path, standard_path)


def write_to_excel(data, sheet_name, NFRs, exp, result_path):
    df = pd.DataFrame()
    try:
        df = pd.read_csv(result_path + "统计_" + sheet_name + ".csv", encoding="utf-8")
    except:
        pass
    df2 = pd.DataFrame(
        [
            {
                "unix_timestamp": data["unix_timestamp"],
                "path": data["path"],
                "fixation_count": data["fixation_count"],
                "duration": data["duration"],
                "fixation_rate": data["fixation_rate"],
                "first_fixation_on_aoi": data["first_fixation_on_aoi"],
                "scan_path_accuracy": data["scan_path_accuracy"],
                "edit_distance": data["edit_distance"],
                "attention_switch": data["attention_switch"],
                "convex_hull": data["convex_hull"],
            }
        ]
    )
    pd.concat([df, df2]).to_csv(
        result_path + "统计_" + sheet_name + ".csv", index=False, encoding="utf-8"
    )

    for NFR in NFRs:
        if exp:
            df_tmp = pd.DataFrame(
                {
                    'Metrics': [
                        'fixation_count',
                        'duration',
                        'fixation_rate',
                        'first_fixation_on_aoi',
                        'scan_path_accuracy',
                        'edit_distance',
                        'attention_switch',
                        'convex_hull',
                    ],
                    'Exp': [
                        data["fixation_count"],
                        data["duration"],
                        data["fixation_rate"],
                        data["first_fixation_on_aoi"],
                        data["scan_path_accuracy"],
                        data["edit_distance"],
                        data["attention_switch"],
                        data["convex_hull"],
                    ],
                    'Standard': ["", "", "", "", "", "", "", ""],
                }
            )
        else:
            df_tmp = pd.DataFrame(
                {
                    'Metrics': [
                        'fixation_count',
                        'duration',
                        'fixation_rate',
                        'first_fixation_on_aoi',
                        'scan_path_accuracy',
                        'edit_distance',
                        'attention_switch',
                        'convex_hull',
                    ],
                    'Exp': ["", "", "", "", "", "", "", ""],
                    'Standard': [
                        data["fixation_count"],
                        data["duration"],
                        data["fixation_rate"],
                        data["first_fixation_on_aoi"],
                        data["scan_path_accuracy"],
                        data["edit_distance"],
                        data["attention_switch"],
                        data["convex_hull"],
                    ],
                }
            )

        try:
            df = pd.read_excel(result_path + "统计" + NFR + ".xlsx")
            pd.concat([df, df_tmp]).to_excel(
                result_path + "统计" + NFR + ".xlsx", index=False
            )
        except:
            df_tmp.to_excel(result_path + "统计" + NFR + ".xlsx", index=False)


# if __name__ == "__main__":
def paint(root_path, time_stamp, result_path):
    file_path = root_path + time_stamp + "/"

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

    with open("./data/AOIs.json", "r") as f:
        AOIs = json.loads(f.read())

    with open("./data/not-relevant-aois.json", "r") as f:
        not_relevant_aois = json.loads(f.read())

    with open("./data/standard-scan-path.json", "r") as f:
        standard_scan_paths = json.loads(f.read())

    results = {}

    # print("|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|".format("unix_timestamp", "path", "fixation_count", "duration",
    #                                                "fixation_rate", "first_fixation_on_aoi", "scan_path_accuracy",
    #                                                "edit_distance",
    #                                                "attention_switch", "convex_hull"))
    # print("|---|---|---|---|---|---|---|---|---|---|")

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

        # 找到路径时间内的相关AOI数据
        path = components[i]["path"]
        if path not in AOIs:
            print("path not in AOIs:", path)
            continue
        AOIs_id = AOIs[path]
        AOIs_size = []
        for AOI_id in AOIs_id:
            tmp_AOI = components[i]["elements"][AOI_id]
            tmp_AOI["name"] = AOI_id
            AOIs_size.append(tmp_AOI)

        # 找到路径时间内不相关的AOI数据
        not_relevant_AOIs = []
        if path not in not_relevant_aois:
            print("path not in not_relevant_aois:", path)
            continue
        not_relevant_AOIs_id = not_relevant_aois[path]
        for AOI_id in not_relevant_AOIs_id:
            tmp_AOI = components[i]["elements"][AOI_id]
            tmp_AOI["name"] = AOI_id
            not_relevant_AOIs.append(tmp_AOI)

        # 找到路径时间内的标准扫描数据
        standard_scan_path = standard_scan_paths[path]

        # 数据处理1：标记fixation和saccade
        time_window_eye_track = mark_fixation_and_saccade(time_window_eye_track)
        # 数据处理2：合并fixation
        time_window_eye_track = merge_multiple_fixations_to_one(time_window_eye_track)

        # 画图
        try:
            im = Image.open(
                file_path + "pic/" + str(components[i]["unix_timestamp"]) + ".jpg"
            )
            draw_AOIs_on_image(im, AOIs_size)
            # im = draw_eye_track_on_image(im, time_window_eye_track)
            draw_eye_track_on_image_with_merged_fixation(im, time_window_eye_track)
            im.save(
                file_path + "pic/" + str(components[i]["unix_timestamp"]) + "_track.jpg"
            )
        except Exception as e:
            print(e)
            pass

        # 计算指标:fixation count & duration & fixation rate & first fixation on aoi

        # print(str(components[i]["unix_timestamp"]),
        #       " fixation count & duration & fixation rate & first fixation on aoi",
        #       count_and_duration_fixation_overlap_aoi(AOIs_size, time_window_eye_track),
        #       " \t\tconvex hull:", calc_convex_hull(time_window_eye_track)["radius"],)

        (
            fixation_count,
            duration,
            fixation_rate,
            first_fixation_on_aoi,
        ) = count_and_duration_fixation_overlap_aoi(AOIs_size, time_window_eye_track)
        convex_hull = calc_convex_hull(time_window_eye_track)
        scan_path = get_scanPath(time_window_eye_track, not_relevant_AOIs)
        attention_switch = calc_attention_switch(scan_path)
        scan_path_accuracy = calc_scan_path_accuracy(scan_path, AOIs_id)
        edit_distance = calc_edit_distance(scan_path, standard_scan_path)
        # print(str(components[i]["unix_timestamp"]), path, "\nfixation_count={}\t\tduration={}\t\tfixation_rate={}\t\tfirst_fixation_on_aoi={}\t\tscan_path_accuracy={}\t\tedit_distance={}\t\tattention_switch={}\t\tconvex_hull={}".format(fixation_count, duration, fixation_rate, first_fixation_on_aoi, scan_path_accuracy, edit_distance, attention_switch, convex_hull["radius"]))
        # print("|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|".format(str(components[i]["unix_timestamp"]), path, fixation_count,
        #                                                duration, fixation_rate, first_fixation_on_aoi,
        #                                                scan_path_accuracy, edit_distance, attention_switch,
        #                                                convex_hull["radius"]))
        # print("scan_path_accuracy="+str(scan_path_accuracy))

        result = {
            "unix_timestamp": str(components[i]["unix_timestamp"]),
            "path": path,
            "fixation_count": fixation_count,
            "duration": duration,
            "fixation_rate": fixation_rate,
            "first_fixation_on_aoi": first_fixation_on_aoi,
            "scan_path_accuracy": scan_path_accuracy,
            "edit_distance": edit_distance,
            "attention_switch": attention_switch,
            "convex_hull": convex_hull["radius"],
        }
        if fixation_count == 0:
            continue

        print(result)

        results[path] = result

    with open(file_path + "BadDesigns.json", "r") as f:
        bad_designs = json.loads(f.read())

    if bad_designs["Accessibility"]:
        if "/expr/MyHome/News" in results:
            write_to_excel(
                results["/expr/MyHome/News"],
                "Accessibility_true",
                ["Accessibility"],
                True,
                result_path,
            )
    else:
        if "/expr/MyHome/News" in results:
            write_to_excel(
                results["/expr/MyHome/News"],
                "Accessibility_false",
                ["Accessibility"],
                False,
                result_path,
            )

    if bad_designs["Ease_of_use"]:
        if "/expr/MyLearning/Booking/SelectDateEaseOfUse" in results:
            write_to_excel(
                results["/expr/MyLearning/Booking/SelectDateEaseOfUse"],
                "Ease_of_use_true",
                ["Ease_of_use"],
                True,
                result_path,
            )
    elif bad_designs["Consistency"]:
        if "/expr/MyLearning/Booking/SelectDateConsistency" in results:
            write_to_excel(
                results["/expr/MyLearning/Booking/SelectDateConsistency"],
                "Consistency_true",
                ["Consistency"],
                True,
                result_path,
            )
    else:
        if "/expr/MyLearning/Booking/SelectDate" in results:
            write_to_excel(
                results["/expr/MyLearning/Booking/SelectDate"],
                "Ease_of_use_&_Consistency_false",
                ["Ease_of_use", "Consistency"],
                False,
                result_path,
            )

    if bad_designs["Accuracy"]:
        if "/expr/MyLearning/Booking/SelectSpace" in results:
            write_to_excel(
                results["/expr/MyLearning/Booking/SelectSpace"],
                "Accuracy_true",
                ["Accuracy"],
                True,
                result_path,
            )
    else:
        if "/expr/MyLearning/Booking/SelectSpace" in results:
            write_to_excel(
                results["/expr/MyLearning/Booking/SelectSpace"],
                "Accuracy_false",
                ["Accuracy"],
                False,
                result_path,
            )

    if bad_designs["Device_efficiency"]:
        if "/expr/MyLearning/Booking/SelectSeatDeviceEfficiency" in results:
            write_to_excel(
                results["/expr/MyLearning/Booking/SelectSeatDeviceEfficiency"],
                "Device_efficiency_true",
                ["Device_efficiency"],
                True,
                result_path,
            )
    elif bad_designs["Robustness"]:
        if "/expr/MyLearning/Booking/SelectSeatRobustness" in results:
            write_to_excel(
                results["/expr/MyLearning/Booking/SelectSeatRobustness"],
                "Robustness_true",
                ["Robustness"],
                True,
                result_path,
            )
    else:
        if "/expr/MyLearning/Booking/SelectSeat" in results:
            write_to_excel(
                results["/expr/MyLearning/Booking/SelectSeat"],
                "Device_efficiency_&_Robustness_false",
                ["Device_efficiency", "Robustness"],
                False,
                result_path,
            )

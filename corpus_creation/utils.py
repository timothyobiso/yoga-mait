import functools
import json
import os.path
import time

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_t = time.perf_counter()
        f_value = func(*args, **kwargs)
        elapsed_t = time.perf_counter() - start_t
        mins = elapsed_t // 60
        print(
            f"'{func.__name__}' elapsed time: {mins} minutes, {elapsed_t - mins * 60:0.2f} seconds"
        )
        return f_value

    return wrapper_timer


def json_loader(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


if __name__ == '__main__':
    data = json_loader("yoga_pose_data.json")
    for pose in data:
        path = "./images/" + pose + ".png"
        if not os.path.isfile(path):
            print(pose, "photo not downloaded")
    for pose, pose_data in data.items():
        print(pose)
        for data_point in pose_data:
            print("\t"+data_point+":", pose_data[data_point])
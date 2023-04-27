from pathlib import Path
from typing import Dict, Union, Generator
import os
import json
import functools
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


def key_to_text(keys: list[str]) -> list[str]:
    """
    Removes underscores from text, e.g. "knee_pile_bind" -> "Knee Pile Bind".
    :param keys:
    :return:
    """
    text = []
    for key in keys:
        word = " ".join([key.capitalize() for key in key.split("_")])
        text.append(word)
    return text


def rename(poses_dict: dict) -> dict:
    """
    Renames dictionary keys in json file, save dictionary as a new json file.
    :param poses_dict:
    :return:
    """
    for pose in poses_dict:
        poses_dict[pose]["name"] = poses_dict[pose]["Pose Name"]
        poses_dict[pose]["description"] = poses_dict[pose]["Pose Description"].replace("  ", " ")
        poses_dict[pose]["benefits"] = poses_dict[pose]["Pose Benefits"].replace("  ", " ")
        poses_dict[pose]["variations_key"] = poses_dict[pose]["Variations"]
        poses_dict[pose]["transitions_into_key"] = poses_dict[pose]["Transitions Into"]
        poses_dict[pose]["transitions_from_key"] = poses_dict[pose]["Transitions From"]
        poses_dict[pose]["variations"] = key_to_text(poses_dict[pose]["Variations"])
        poses_dict[pose]["transitions_into"] = key_to_text(poses_dict[pose]["Transitions Into"])
        poses_dict[pose]["transitions_from"] = key_to_text(poses_dict[pose]["Transitions From"])
        poses_dict[pose]["difficulty"] = poses_dict[pose]["Difficulty"]
        poses_dict[pose]["category"] = [cat for cat in poses_dict[pose]["Category"].split(" / ")]
        del poses_dict[pose]["Pose Name"], poses_dict[pose]["Pose Benefits"], poses_dict[pose]["Pose Description"], \
            poses_dict[pose]["Variations"], poses_dict[pose]["Transitions Into"], poses_dict[pose]["Transitions From"], \
            poses_dict[pose]["Difficulty"], poses_dict[pose]["Category"]
    with open('data/data_updated.json', 'w') as f:
        # creare a new json file with new keys
        json.dump(poses_dict, f)
    return poses_dict


def load_poses(poses_folder_path: Union[str, os.PathLike]) -> Generator[Dict, None, None]:
    # prepare and load the poses for ES indexing
    poses_folder_path = Path(poses_folder_path)
    poses_docs_path = poses_folder_path.joinpath("yoga_pose_data.json")

    with open(poses_docs_path, "r", encoding="utf-8") as f:
        for line in f:
            poses_dict = json.loads(line)
            poses_dict_updated = rename(poses_dict)
            for i, pose in enumerate(poses_dict_updated):
                pose_dict = poses_dict_updated[pose]
                pose_dict["_id"] = i
                yield pose_dict


if __name__ == "__main__":
    pass


from typing import Dict
import json


def get_pose(anchor: str) -> Dict:
    # TODO: Method that returns dictionary of info associated with a pose from its (unique) anchor
    with open('data/data_updated.json') as f:
        data = json.load(f)
        return data[anchor]

def get_poses(poses):
    print(poses[0])
    return [get_pose(pose.lower().replace(" pose","").replace(" ", "_")) for pose in poses[:1]]

def string_to_list(string):
    lines = string.strip().split('\n')
    items = [line.split('. ')[1] for line in lines]
    return items
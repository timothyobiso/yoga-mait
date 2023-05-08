# Preprocessing of data scraped by Justin Lewman
# Developed by Anastasiia Tatlubaeva

import json, os


def from_key_to_text(keys: list[str]) -> list[str]:
    text = []
    for key in keys:
        split_key = key.split("_")
        text.append(" ".join([word.capitalize() for word in split_key]))
    return text


def rename(pose_anchor: str, pose_dict: dict) -> dict:
    """
    Helper function that:
     - renames certain fields.
     - adds new fields based on old fields.
    :param pose_anchor:
    :param pose_dict:
    :return:
    """
    pose_dict["name"] = pose_dict["Pose Name"]
    pose_dict["description"] = pose_dict["Pose Description"].replace("  ", " ")
    pose_dict["benefits"] = pose_dict["Pose Benefits"].replace("  ", " ")
    pose_dict["variations_key"] = pose_dict["Variations"]
    pose_dict["transitions_into_key"] = pose_dict["Transitions Into"]
    pose_dict["transitions_from_key"] = pose_dict["Transitions From"]
    pose_dict["variations"] = from_key_to_text(pose_dict["Variations"])
    pose_dict["transitions_into"] = from_key_to_text(pose_dict["Transitions Into"])
    pose_dict["transitions_from"] = from_key_to_text(pose_dict["Transitions From"])
    pose_dict["difficulty"] = pose_dict["Difficulty"]
    pose_dict["category"] = pose_dict["Category"].split(" / ")
    pose_dict["anchor"] = pose_anchor
    del pose_dict["Pose Name"], pose_dict["Pose Description"], pose_dict["Pose Benefits"],\
        pose_dict["Variations"], pose_dict["Transitions Into"], pose_dict["Transitions From"], \
        pose_dict["Difficulty"], pose_dict["Category"]
    return pose_dict


if __name__ == '__main__':
    # Absolute path of parent directory
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    # Path to data
    data_dir = os.path.join(parent_dir, "data", "yoga_pose_data.json")

    with open(data_dir, 'r') as f:
        data = json.load(f)  # Load original data
        for pose in data:
            data[pose] = rename(pose, data[pose])  # Preprocessing

    # Destination path
    output_dir = os.path.join(parent_dir, "data", "data_updated.json")
    with open(output_dir, 'w') as f:
        json.dump(data, f)  # Save modified data

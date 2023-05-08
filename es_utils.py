# Loads json file with our data, prepares it to be uploaded into Elasticsearch
# Developed by Anastasiia Tatlubaeva

from pathlib import Path
from typing import Dict, Union, Generator
import os
import json
import functools
import time
from embedding_service.client import EmbeddingClient

encoder = EmbeddingClient(host="localhost", embedding_type="sbert")


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


def load_poses(poses_folder_path: Union[str, os.PathLike]) -> Generator[Dict, None, None]:
    # Prepare and load the poses for ES indexing
    poses_folder_path = Path(poses_folder_path)
    poses_docs_path = poses_folder_path.joinpath("data_updated.json")

    with open(poses_docs_path, "r", encoding="utf-8") as f:
        for line in f:
            poses_dict = json.loads(line)
            for i, pose in enumerate(poses_dict):
                pose_dict = poses_dict[pose]
                pose_dict["anchor"] = pose
                pose_dict["_id"] = i
                description_diff = [pose_dict["description"] + pose_dict["difficulty"]]
                benefits_diff = [pose_dict["benefits"] + pose_dict["difficulty"]]
                pose_dict["name_embedding"] = encoder.encode([pose_dict["name"]]).tolist()[0]
                pose_dict["description_embedding"] = encoder.encode(description_diff).tolist()[0]
                pose_dict["benefits_embedding"] = encoder.encode(benefits_diff).tolist()[0]
                yield pose_dict


if __name__ == "__main__":
    pass


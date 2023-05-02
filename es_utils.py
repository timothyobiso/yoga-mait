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


def embeddings(description: str, benefits: str):
    text = [description] + [benefits]
    embedding = encoder.encode(text)
    return embedding


def load_poses(poses_folder_path: Union[str, os.PathLike]) -> Generator[Dict, None, None]:
    # prepare and load the poses for ES indexing
    poses_folder_path = Path(poses_folder_path)
    poses_docs_path = poses_folder_path.joinpath("data_updated.json")

    with open(poses_docs_path, "r", encoding="utf-8") as f:
        for line in f:
            poses_dict = json.loads(line)
            for i, pose in enumerate(poses_dict):
                pose_dict = poses_dict[pose]
                pose_dict["_id"] = i
                text = [pose_dict["description"] + pose_dict["benefits"]]
                pose_dict["sbert_embedding"] = encoder.encode(text).tolist()[0]
                yield pose_dict


if __name__ == "__main__":
    pass


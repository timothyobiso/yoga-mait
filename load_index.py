import argparse
import time
from typing import List, Dict, Union, Iterator
from es_service.index import ESIndex
from es_utils import load_poses
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


class IndexLoader:
    """
    load document index to Elasticsearch
    """

    def __init__(self, index, poses):

        self.index_name = index
        self.poses: Union[Iterator[Dict], List[Dict]] = poses

    def load(self) -> None:
        st = time.time()
        logger.info(f"Building index ...")
        ESIndex(self.index_name, self.poses)
        logger.info(
            f"=== Built {self.index_name} in {round(time.time() - st, 2)} seconds ==="
        )

    @classmethod
    def from_folder(cls, index_name: str, poses_folder_path: str) -> "IndexLoader":
        try:
            return IndexLoader(index_name, load_poses(poses_folder_path))
        except FileNotFoundError:
            raise Exception(f"Cannot find {poses_folder_path}!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--index_name",
        required=True,
        type=str,
        help="name of the ES index",
    )
    parser.add_argument(
        "--poses_folder_path",
        required=True,
        type=str,
        help="path to the poses folder",
    )

    args = parser.parse_args()
    idx_loader = IndexLoader.from_folder(args.index_name, args.poses_folder_path)
    idx_loader.load()


if __name__ == "__main__":
    main()

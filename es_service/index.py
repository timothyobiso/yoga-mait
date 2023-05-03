from typing import Iterator, Dict, Union, Sequence, Generator

from elasticsearch_dsl import Index  # type: ignore

from elasticsearch_dsl.connections import connections  # type: ignore
from elasticsearch.helpers import bulk

from es_service.doc_template import BasePose


class ESIndex(object):
    def __init__(
        self,
        index_name: str,
        poses: Union[Iterator[Dict], Sequence[Dict]],
    ):
        """
        ES index structure
        :param index_name: index name
        :param poses: poses to be loaded
        """
        # set an elasticsearch connection to localhost
        connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
        self.index = index_name
        es_index = Index(self.index)  # initialize the index

        # delete existing index that has the same name
        if es_index.exists():
            es_index.delete()

        es_index.document(BasePose)  # link document mapping to the index
        es_index.create()  # create the index
        if poses is not None:
            self.load(poses)

    @staticmethod
    def _populate_doc(
        poses: Union[Iterator[Dict], Sequence[Dict]]
    ) -> Generator[BasePose, None, None]:
        """
        populate the BasePose
        :param poses: poses
        :return:
        """
        for i, pose in enumerate(poses):
            es_pose = BasePose(_id=i)
            es_pose.doc_id = pose["_id"]
            es_pose.name = pose["name"]
            es_pose.name_embedding = pose["name_embedding"]
            es_pose.anchor = pose["anchor"]
            es_pose.description = pose["description"]
            es_pose.description_embedding = pose["description_embedding"]
            es_pose.benefits = pose["benefits"]
            es_pose.benefits_embedding = pose["benefits_embedding"]
            es_pose.variations = pose["variations"]
            es_pose.transitions_into = pose["transitions_into"]
            es_pose.transitions_from = pose["transitions_from"]
            es_pose.variations_key = pose["variations_key"]
            es_pose.transitions_into_key = pose["transitions_into_key"]
            es_pose.transitions_from_key = pose["transitions_from_key"]
            es_pose.difficulty = pose["difficulty"]
            es_pose.category = pose["category"]
            es_pose.sbert_embedding = pose["sbert_embedding"]
            yield es_pose

    def load(self, poses: Union[Iterator[Dict], Sequence[Dict]]):
        # bulk insertion
        bulk(
            connections.get_connection(),
            (
                d.to_dict(
                    include_meta=True, skip_empty=False
                )  # serialize the BasePose instance (include meta information and not skip empty documents)
                for d in self._populate_doc(poses)
            ),
        )

# Adapted from ps5 by Anastasiia Tatlubaeva
# Creates a template for a single document in Elasticsearch database "poses'

from elasticsearch_dsl import (  # type: ignore
    Document,
    Text,
    Keyword,
    DenseVector,
    analyzer,
    tokenizer
)


class BasePose(Document):
    """
    pose mapping structure
    """

    doc_id = (
        Keyword()
    )  # the doc_id is treated as a Keyword (its value won't be tokenized or normalized).
    name = Text(
        analyzer="snowball"
    )
    name_embedding = DenseVector(
        dims=768
    )  # sentence BERT embedding of "name"
    anchor = (
        Keyword()
    )  # original html anchor text (for navigation)
    description = Text(
        analyzer="snowball"
    )
    description_embedding = DenseVector(
        dims=768
    )  # sentence BERT embedding
    benefits = Text(
        analyzer="snowball"
    )
    benefits_embedding = DenseVector(
        dims=768
    )  # sentence BERT embedding
    variations = Text(
        analyzer="snowball",
        multi=True
    )  # list of variations in Text format
    transitions_into = Text(
        analyzer="snowball",
        multi=True
    )  # list of poses to transition into in Text format
    transitions_from = Text(
        analyzer="snowball",
        multi=True
    )  # list of poses to transition from in Text format
    variations_key = Keyword(
        multi=True
    )  # list of variations in Text format in Keyword format
    transitions_into_key = Keyword(
        multi=True
    )  # list of poses to transition into in Keyword format
    transitions_from_key = Keyword(
        multi=True
    )  # list of poses to transition from in Keyword format
    difficulty = Text(
        analyzer="snowball"
    )  # difficulty of the pose
    category = Keyword(
        multi=True
    )  # broader pose category

    def save(self, *args, **kwargs):
        """
        save an instance of this document mapping in the index
        this function is not called because we are doing bulk insertion to the index in the index.py
        """
        return super(BasePose, self).save(*args, **kwargs)


if __name__ == "__main__":
    pass

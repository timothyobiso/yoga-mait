from elasticsearch_dsl import (  # type: ignore
    Document,
    Text,
    Keyword,
    DenseVector,
    Date,
    token_filter,
    analyzer,
    tokenizer,
    Nested,
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
    )  # by default, Text field will be applied a standard analyzer at both index and search time
    name_embedding = DenseVector(
        dims=768
    )  # sentence BERT embedding in the DenseVector field
    anchor = (
        Keyword()
    )
    description = Text(
        analyzer="snowball"
    )
    description_embedding = DenseVector(
        dims=768
    )  # sentence BERT embedding in the DenseVector field
    benefits = Text(
        analyzer="snowball"
    )
    benefits_embedding = DenseVector(
        dims=768
    )  # sentence BERT embedding in the DenseVector field
    variations = Text(
        analyzer="snowball",
        multi=True
    )
    transitions_into = Text(
        analyzer="snowball",
        multi=True
    )
    transitions_from = Text(
        analyzer="snowball",
        multi=True
    )
    variations_key = Keyword(
        multi=True
    )  # to perform exact matches on the strings (variations) and treat them as individual terms
    transitions_into_key = Keyword(
        multi=True
    )
    transitions_from_key = Keyword(
        multi=True
    )
    difficulty = Text(
        analyzer="snowball"
    )
    category = Keyword(
        multi=True
    )

    def save(self, *args, **kwargs):
        """
        save an instance of this document mapping in the index
        this function is not called because we are doing bulk insertion to the index in the index.py
        """
        return super(BasePose, self).save(*args, **kwargs)


if __name__ == "__main__":
    pass

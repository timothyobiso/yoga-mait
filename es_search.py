# Search function for "poses" database
# Developed by Anaastasiia Tatlubaeva

from elasticsearch_dsl import Search
from typing import Tuple
from embedding_service.client import EmbeddingClient
from elasticsearch import Elasticsearch

encoder = EmbeddingClient(host="localhost", embedding_type="sbert")
es = Elasticsearch()


class SearchIndex:

    @staticmethod
    def embed_query(query_text: str, category: str):
        """
        Creates an embeddings for the text of the query.
        """
        query_vector = encoder.encode([query_text]).tolist()[0]  # Encode text of the query
        embedding = category + "_embedding"
        q_vector = {
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, params.embedding) + 1.0",
                        # +1.0 to avoid negative score
                        "params": {"query_vector": query_vector, "embedding": embedding}
                    }
                }
            },
        }  # Create a vector query
        return q_vector

    @staticmethod
    def create_query(query_text: str, category: str) -> dict:
        """
        Based on search category, create a query object (dictionary) from the text of the query.
        "name" queries are "match-phrase" queries, "description" and "benefits" queries use sbert embeddings.
        """
        if category == "name":
            # Return poses whose name matches the text of the query.
            query = {
                "query": {
                    "match_phrase": {
                        "name": {
                            "query": query_text,
                        }
                    }
                },
                "analyzer": "snowball"
            }
        else:
            query = SearchIndex.embed_query(query_text, category)
        return query

    @classmethod
    def search_index(cls, query_text: str, category: str) -> Tuple[list, bool]:
        """
        Takes the text of query and search category, returns a tuple with a list of poses that best
        match the query and a boolean whose value is True if keyword search by 'name' failed and
        False otherwise.
        """
        fail = False

        query = cls.create_query(query_text, category)  # Create a query
        s = Search(index="poses").query(query['query'])[:10]  # Search the index for top 10 matches
        response = s.execute()

        if category == "name" and not response:
            # If a pose with the exact 'name' is not found, embed the query and use cosine similarity to find
            # the best possible match.
            fail = True
            query = cls.embed_query(query_text, category)
            s = Search(index="poses").query(query['query'])[:10]  # Search the index for top 10 matches
            response = s.execute()

        return response, fail


if __name__ == '__main__':
    pass


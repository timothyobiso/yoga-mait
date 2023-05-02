from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from embedding_service.client import EmbeddingClient
from elasticsearch import Elasticsearch

encoder = EmbeddingClient(host="localhost", embedding_type="sbert")
es = Elasticsearch()


class SearchIndex:

    @staticmethod
    def create_query(query_text: str, category: str) -> dict:
        if category == "name":
            # Returns poses whose name matches the query. If the name does not match, but one of the poses
            # listed in variations does, its score is increased. E.g. query "chair" will also return "Figure
            # Four" because it lists chair-like poses in its variations.
            query = {
                        "query": {
                            "bool": {
                                "should": [
                                    {
                                        "match": {
                                            "name": {
                                                "query": query_text,
                                                "boost": 2
                                            }
                                        }
                                    },
                                    {
                                        "match": {
                                            "variations": {
                                                "query": query_text,
                                                "boost": 1
                                            }
                                        }
                                    }
                                ]
                            }
                        },
                        "index": "poses"
                    }
        elif category == "description" or category == "benefits":
            # Returns poses whose description matches the query.
            query = {
                        "query": {
                            "match": {
                                category: {
                                    "query": query_text,
                                    "minimum_should_match": "75%"
                                }
                            }
                        },
                        "index": "poses"
                    }
        elif category == "difficulty":
            query = {
                "query": {
                    "match": {
                        "difficulty": query_text
                    }
                }
            }
        else:
            # transitions_from, transitions_into, category, variations
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "terms": {
                                    category: [query_text]
                                }
                            }
                        ]
                    }
                }
            }
        return query

    @staticmethod
    def embed_query(query_text: str):
        query_vector = encoder.encode([query_text]).tolist()[0]  # Get the query embedding and convert it to a list
        q_vector = {
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'sbert_embedding') + 1.0",
                        # +1.0 to avoid negative score
                        "params": {"query_vector": query_vector}
                    }
                }
            },
        }
        return q_vector


    @classmethod
    def search_index(cls, query_text: str, category: str, embed=False) -> list:
        """
        Takes a list of queries
        """
        query = cls.embed_query(query_text) if embed else cls.create_query(query_text, category)
        s = Search(index="poses").query(query['query'])[:8]  # Search the index for top 10 matches
        response = s.execute()
        return response


if __name__ == '__main__':
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    search = SearchIndex.search_index("easy pose for back pain", "-", embed=True)
    for res in search:
        print(
            res.name, res.difficulty, res.description, res.benefits, sep="\t"
        )


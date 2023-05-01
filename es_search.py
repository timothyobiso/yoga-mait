from elasticsearch_dsl import Search


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

    @classmethod
    def search_index(cls, query_text: str, category: str) -> list:
        """
        Takes a list of queries
        """
        query = cls.create_query(query_text, category)
        s = Search(index="poses").query(query['query'])[:8]  # Search the index for top 10 matches
        response = s.execute()
        return response


if __name__ == '__main__':
    #connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    #search = SearchIndex.search_index("chair", "transitions_into")
    """
    for res in search:
        print(
            res.name, res.transitions_into, sep="\t"
        )
    """


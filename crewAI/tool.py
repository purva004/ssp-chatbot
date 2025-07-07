from neo4j import GraphDatabase
from typing import Any

class Neo4jQueryTool:
    """Tool for executing Cypher queries against Neo4j database."""
    
    def __init__(self):
        self.name = "neo4j_query_tool"
        self.description = "Execute Cypher queries against Neo4j database to retrieve occupancy data. Input should be a valid Cypher query string."
    
    def _run(self, query: str) -> str:
        """Execute a Cypher query against the Neo4j database."""
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "purva@1234"

        driver = GraphDatabase.driver(uri, auth=(username, password))
        result_string = ""

        try:
            with driver.session() as session:
                result = session.run(query)
                records = list(result)
                if records:
                    for record in records:
                        result_string += str(record.data()) + "\n"
                else:
                    result_string = "No results found for this query."
        except Exception as e:
            result_string = f"Neo4j Error: {str(e)}"
        finally:
            driver.close()

        return result_string.strip()

# Create an instance of the tool
neo4j_query_tool = Neo4jQueryTool()

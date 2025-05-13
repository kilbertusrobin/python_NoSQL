from py2neo import Graph
import os

# Configuration Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Instance de la base de données Neo4j
_graph = None

def get_db():
    """Récupérer une instance de la base de données Neo4j"""
    global _graph
    if _graph is None:
        _graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return _graph

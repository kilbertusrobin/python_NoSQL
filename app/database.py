from py2neo import Graph
from .config import Config

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            try:
                cls._instance.graph = Graph(
                    Config.NEO4J_URI, 
                    auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
                )
                print("Connected to Neo4j database")
            except Exception as e:
                print(f"Failed to connect to Neo4j: {e}")
                cls._instance.graph = None
        return cls._instance

    def get_db(self):
        return self.graph

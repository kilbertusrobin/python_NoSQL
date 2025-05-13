import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env s'il existe
load_dotenv()

class Config:
    # Configuration Neo4j
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')
    
    # Configuration Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key_should_be_changed_in_production')
    DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')

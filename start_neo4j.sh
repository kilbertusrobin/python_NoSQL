#!/bin/bash
echo "Démarrage de Neo4j avec Docker..."
docker run --name neo4j -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:4.4

echo "Neo4j est démarré. Interface web disponible sur http://localhost:7474"
echo "  Username: neo4j"
echo "  Password: password"

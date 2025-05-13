from app import db
from py2neo import Node, Relationship
import uuid
import time

class User:
    def __init__(self, name=None, email=None, user_id=None):
        self.name = name
        self.email = email
        self.id = user_id or str(uuid.uuid4())
        self.created_at = int(time.time() * 1000)  # timestamp en millisecondes
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at
        }
    
    @staticmethod
    def from_node(node):
        """Convertit un nœud Neo4j en objet User"""
        if not node:
            return None
        user = User()
        user.id = node.get("id")
        user.name = node.get("name")
        user.email = node.get("email")
        user.created_at = node.get("created_at")
        return user
    
    def save(self):
        """Crée ou met à jour un utilisateur dans la base de données"""
        user_node = Node("User", 
                        id=self.id, 
                        name=self.name, 
                        email=self.email, 
                        created_at=self.created_at)
        db.merge(user_node, "User", "id")
        return self
    
    @staticmethod
    def find_by_id(user_id):
        """Trouve un utilisateur par son ID"""
        query = """
        MATCH (u:User {id: })
        RETURN u
        """
        result = db.run(query, user_id=user_id).data()
        if result:
            return User.from_node(result[0].get('u'))
        return None
    
    @staticmethod
    def find_all():
        """Récupère tous les utilisateurs"""
        query = """
        MATCH (u:User)
        RETURN u
        ORDER BY u.created_at DESC
        """
        results = db.run(query).data()
        return [User.from_node(record.get('u')) for record in results]
    
    @staticmethod
    def delete(user_id):
        """Supprime un utilisateur et toutes ses relations"""
        query = """
        MATCH (u:User {id: })
        OPTIONAL MATCH (u)-[r]-()
        DELETE r, u
        """
        db.run(query, user_id=user_id)
        return True
    
    def add_friend(self, friend_id):
        """Ajoute une relation d'amitié avec un autre utilisateur"""
        query = """
        MATCH (u1:User {id: }), (u2:User {id: })
        MERGE (u1)-[r:FRIENDS_WITH]->(u2)
        RETURN r
        """
        result = db.run(query, user_id=self.id, friend_id=friend_id).data()
        return bool(result)
    
    def remove_friend(self, friend_id):
        """Supprime une relation d'amitié"""
        query = """
        MATCH (u1:User {id: })-[r:FRIENDS_WITH]-(u2:User {id: })
        DELETE r
        """
        db.run(query, user_id=self.id, friend_id=friend_id)
        return True
    
    def get_friends(self):
        """Récupère la liste des amis de l'utilisateur"""
        query = """
        MATCH (u:User {id: })-[:FRIENDS_WITH]-(friend:User)
        RETURN friend
        """
        results = db.run(query, user_id=self.id).data()
        return [User.from_node(record.get('friend')) for record in results]
    
    @staticmethod
    def check_friendship(user_id, friend_id):
        """Vérifie si deux utilisateurs sont amis"""
        query = """
        MATCH (u1:User {id: })-[r:FRIENDS_WITH]-(u2:User {id: })
        RETURN r
        """
        result = db.run(query, user_id=user_id, friend_id=friend_id).data()
        return bool(result)
    
    @staticmethod
    def get_mutual_friends(user_id, other_id):
        """Récupère les amis en commun entre deux utilisateurs"""
        query = """
        MATCH (u1:User {id: })-[:FRIENDS_WITH]-(mutual:User)-[:FRIENDS_WITH]-(u2:User {id: })
        RETURN mutual
        """
        results = db.run(query, user_id=user_id, other_id=other_id).data()
        return [User.from_node(record.get('mutual')) for record in results]

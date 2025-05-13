from app import db
from py2neo import Node, Relationship
import uuid
import time
from .user import User

class Post:
    def __init__(self, title=None, content=None, user_id=None, post_id=None):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.id = post_id or str(uuid.uuid4())
        self.created_at = int(time.time() * 1000)  # timestamp en millisecondes
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "created_at": self.created_at
        }
    
    @staticmethod
    def from_node(node):
        """Convertit un nœud Neo4j en objet Post"""
        if not node:
            return None
        post = Post()
        post.id = node.get("id")
        post.title = node.get("title")
        post.content = node.get("content")
        post.created_at = node.get("created_at")
        return post
    
    def save(self):
        """Crée ou met à jour un post dans la base de données"""
        # Vérifier si l'utilisateur existe
        user = User.find_by_id(self.user_id)
        if not user:
            raise ValueError(f"Utilisateur avec l'ID {self.user_id} non trouvé")
        
        # Créer ou mettre à jour le post
        post_node = Node("Post", 
                         id=self.id, 
                         title=self.title, 
                         content=self.content, 
                         created_at=self.created_at)
        
        # Fusionner le nœud du post en utilisant l'ID comme clé
        db.merge(post_node, "Post", "id")
        
        # Créer la relation entre l'utilisateur et le post s'il s'agit d'un nouveau post
        query = """
        MATCH (u:User {id: }), (p:Post {id: })
        MERGE (u)-[r:CREATED]->(p)
        RETURN r
        """
        db.run(query, user_id=self.user_id, post_id=self.id)
        
        return self
    
    @staticmethod
    def find_by_id(post_id):
        """Trouve un post par son ID"""
        query = """
        MATCH (p:Post {id: })
        OPTIONAL MATCH (u:User)-[:CREATED]->(p)
        RETURN p, u.id as user_id
        """
        result = db.run(query, post_id=post_id).data()
        if result:
            post = Post.from_node(result[0].get('p'))
            post.user_id = result[0].get('user_id')
            return post
        return None
    
    @staticmethod
    def find_all():
        """Récupère tous les posts"""
        query = """
        MATCH (u:User)-[:CREATED]->(p:Post)
        RETURN p, u.id as user_id
        ORDER BY p.created_at DESC
        """
        results = db.run(query).data()
        posts = []
        for record in results:
            post = Post.from_node(record.get('p'))
            post.user_id = record.get('user_id')
            posts.append(post)
        return posts
    
    @staticmethod
    def find_by_user(user_id):
        """Récupère tous les posts d'un utilisateur"""
        query = """
        MATCH (u:User {id: })-[:CREATED]->(p:Post)
        RETURN p
        ORDER BY p.created_at DESC
        """
        results = db.run(query, user_id=user_id).data()
        posts = []
        for record in results:
            post = Post.from_node(record.get('p'))
            post.user_id = user_id
            posts.append(post)
        return posts
    
    @staticmethod
    def delete(post_id):
        """Supprime un post et toutes ses relations"""
        query = """
        MATCH (p:Post {id: })
        OPTIONAL MATCH (p)-[r]-()
        DELETE r, p
        """
        db.run(query, post_id=post_id)
        return True
    
    def like(self, user_id):
        """Ajoute un like à un post"""
        query = """
        MATCH (u:User {id: }), (p:Post {id: })
        MERGE (u)-[r:LIKES]->(p)
        RETURN r
        """
        result = db.run(query, user_id=user_id, post_id=self.id).data()
        return bool(result)
    
    def unlike(self, user_id):
        """Retire un like d'un post"""
        query = """
        MATCH (u:User {id: })-[r:LIKES]->(p:Post {id: })
        DELETE r
        """
        db.run(query, user_id=user_id, post_id=self.id)
        return True
    
    def get_likes_count(self):
        """Récupère le nombre de likes d'un post"""
        query = """
        MATCH (u:User)-[:LIKES]->(p:Post {id: })
        RETURN count(u) as likes_count
        """
        result = db.run(query, post_id=self.id).data()
        return result[0].get('likes_count') if result else 0
    
    def get_liked_by(self):
        """Récupère les utilisateurs qui ont aimé ce post"""
        query = """
        MATCH (u:User)-[:LIKES]->(p:Post {id: })
        RETURN u
        """
        results = db.run(query, post_id=self.id).data()
        return [User.from_node(record.get('u')) for record in results]

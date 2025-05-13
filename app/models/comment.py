from app import db
from py2neo import Node, Relationship
import uuid
import time
from .user import User

class Comment:
    def __init__(self, content=None, user_id=None, post_id=None, comment_id=None):
        self.content = content
        self.user_id = user_id
        self.post_id = post_id
        self.id = comment_id or str(uuid.uuid4())
        self.created_at = int(time.time() * 1000)  # timestamp en millisecondes
    
    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at
        }
    
    @staticmethod
    def from_node(node):
        """Convertit un nœud Neo4j en objet Comment"""
        if not node:
            return None
        comment = Comment()
        comment.id = node.get("id")
        comment.content = node.get("content")
        comment.created_at = node.get("created_at")
        return comment
    
    def save(self):
        """Crée ou met à jour un commentaire dans la base de données"""
        # Vérifier si l'utilisateur et le post existent
        from .post import Post
        
        user = User.find_by_id(self.user_id)
        post = Post.find_by_id(self.post_id)
        
        if not user:
            raise ValueError(f"Utilisateur avec l'ID {self.user_id} non trouvé")
        if not post:
            raise ValueError(f"Post avec l'ID {self.post_id} non trouvé")
        
        # Créer ou mettre à jour le commentaire
        comment_node = Node("Comment", 
                           id=self.id, 
                           content=self.content, 
                           created_at=self.created_at)
        
        # Fusionner le nœud du commentaire en utilisant l'ID comme clé
        db.merge(comment_node, "Comment", "id")
        
        # Créer les relations entre l'utilisateur, le post et le commentaire
        query = """
        MATCH (u:User {id: }), (p:Post {id: }), (c:Comment {id: })
        MERGE (u)-[r1:CREATED]->(c)
        MERGE (p)-[r2:HAS_COMMENT]->(c)
        RETURN r1, r2
        """
        db.run(query, user_id=self.user_id, post_id=self.post_id, comment_id=self.id)
        
        return self
    
    @staticmethod
    def find_by_id(comment_id):
        """Trouve un commentaire par son ID"""
        query = """
        MATCH (c:Comment {id: })
        OPTIONAL MATCH (u:User)-[:CREATED]->(c)
        OPTIONAL MATCH (p:Post)-[:HAS_COMMENT]->(c)
        RETURN c, u.id as user_id, p.id as post_id
        """
        result = db.run(query, comment_id=comment_id).data()
        if result:
            comment = Comment.from_node(result[0].get('c'))
            comment.user_id = result[0].get('user_id')
            comment.post_id = result[0].get('post_id')
            return comment
        return None
    
    @staticmethod
    def find_all():
        """Récupère tous les commentaires"""
        query = """
        MATCH (u:User)-[:CREATED]->(c:Comment)<-[:HAS_COMMENT]-(p:Post)
        RETURN c, u.id as user_id, p.id as post_id
        ORDER BY c.created_at DESC
        """
        results = db.run(query).data()
        comments = []
        for record in results:
            comment = Comment.from_node(record.get('c'))
            comment.user_id = record.get('user_id')
            comment.post_id = record.get('post_id')
            comments.append(comment)
        return comments
    
    @staticmethod
    def find_by_post(post_id):
        """Récupère tous les commentaires d'un post"""
        query = """
        MATCH (p:Post {id: })-[:HAS_COMMENT]->(c:Comment)
        MATCH (u:User)-[:CREATED]->(c)
        RETURN c, u.id as user_id
        ORDER BY c.created_at DESC
        """
        results = db.run(query, post_id=post_id).data()
        comments = []
        for record in results:
            comment = Comment.from_node(record.get('c'))
            comment.user_id = record.get('user_id')
            comment.post_id = post_id
            comments.append(comment)
        return comments
    
    @staticmethod
    def delete(comment_id):
        """Supprime un commentaire et toutes ses relations"""
        query = """
        MATCH (c:Comment {id: })
        OPTIONAL MATCH (c)-[r]-()
        DELETE r, c
        """
        db.run(query, comment_id=comment_id)
        return True
    
    def like(self, user_id):
        """Ajoute un like à un commentaire"""
        query = """
        MATCH (u:User {id: }), (c:Comment {id: })
        MERGE (u)-[r:LIKES]->(c)
        RETURN r
        """
        result = db.run(query, user_id=user_id, comment_id=self.id).data()
        return bool(result)
    
    def unlike(self, user_id):
        """Retire un like d'un commentaire"""
        query = """
        MATCH (u:User {id: })-[r:LIKES]->(c:Comment {id: })
        DELETE r
        """
        db.run(query, user_id=user_id, comment_id=self.id)
        return True
    
    def get_likes_count(self):
        """Récupère le nombre de likes d'un commentaire"""
        query = """
        MATCH (u:User)-[:LIKES]->(c:Comment {id: })
        RETURN count(u) as likes_count
        """
        result = db.run(query, comment_id=self.id).data()
        return result[0].get('likes_count') if result else 0

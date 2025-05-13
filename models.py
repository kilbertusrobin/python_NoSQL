import uuid
from datetime import datetime
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from py2neo import Node, Relationship
from database import get_db

class BaseModel:
    """Classe de base pour tous les modèles"""
    
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        """Convertir l'objet en dictionnaire"""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    def save(self):
        """Sauvegarder l'objet dans la base de données"""
        db = get_db()
        node = Node(self.__class__.__name__, **self.to_dict())
        db.create(node)
        return self
    
    @classmethod
    def find_by_id(cls, id):
        """Trouver un objet par son ID"""
        db = get_db()
        node = db.nodes.match(cls.__name__, id=id).first()
        if node:
            obj = cls()
            for key, value in dict(node).items():
                setattr(obj, key, value)
            return obj
        return None
    
    @classmethod
    def find_all(cls):
        """Trouver tous les objets"""
        db = get_db()
        nodes = db.nodes.match(cls.__name__)
        result = []
        for node in nodes:
            obj = cls()
            for key, value in dict(node).items():
                setattr(obj, key, value)
            result.append(obj)
        return result
    
    def update(self, **kwargs):
        """Mettre à jour l'objet"""
        db = get_db()
        node = db.nodes.match(self.__class__.__name__, id=self.id).first()
        if node:
            for key, value in kwargs.items():
                if key not in ['id', 'created_at']:
                    node[key] = value
                    setattr(self, key, value)
            db.push(node)
        return self
    
    def delete(self):
        """Supprimer l'objet"""
        db = get_db()
        node = db.nodes.match(self.__class__.__name__, id=self.id).first()
        if node:
            db.delete(node)
        return True

class User(BaseModel):
    """Modèle pour les utilisateurs"""
    
    def __init__(self, name=None, email=None):
        super().__init__()
        self.name = name
        self.email = email
    
    def add_friend(self, friend_id):
        """Ajouter un ami"""
        db = get_db()
        user_node = db.nodes.match("User", id=self.id).first()
        friend_node = db.nodes.match("User", id=friend_id).first()
        
        if user_node and friend_node:
            rel = Relationship(user_node, "FRIENDS_WITH", friend_node)
            db.create(rel)
            return True
        return False
    
    def remove_friend(self, friend_id):
        """Supprimer un ami"""
        db = get_db()
        query = """
        MATCH (u:User {id: $user_id})-[r:FRIENDS_WITH]-(f:User {id: $friend_id})
        DELETE r
        """
        db.run(query, user_id=self.id, friend_id=friend_id)
        return True
    
    def is_friend_with(self, friend_id):
        """Vérifier si deux utilisateurs sont amis"""
        db = get_db()
        query = """
        MATCH (u:User {id: $user_id})-[:FRIENDS_WITH]-(f:User {id: $friend_id})
        RETURN f
        """
        result = db.run(query, user_id=self.id, friend_id=friend_id).data()
        return len(result) > 0
    
    def get_friends(self):
        """Récupérer la liste des amis d'un utilisateur"""
        db = get_db()
        query = """
        MATCH (u:User {id: $user_id})-[:FRIENDS_WITH]-(f:User)
        RETURN f
        """
        result = db.run(query, user_id=self.id).data()
        friends = []
        for record in result:
            friend = User()
            for key, value in record['f'].items():
                setattr(friend, key, value)
            friends.append(friend)
        return friends
    
    def get_mutual_friends(self, other_id):
        """Récupérer les amis en commun"""
        db = get_db()
        query = """
        MATCH (u1:User {id: $user_id})-[:FRIENDS_WITH]-(f:User)-[:FRIENDS_WITH]-(u2:User {id: $other_id})
        RETURN f
        """
        result = db.run(query, user_id=self.id, other_id=other_id).data()
        mutual_friends = []
        for record in result:
            friend = User()
            for key, value in record['f'].items():
                setattr(friend, key, value)
            mutual_friends.append(friend)
        return mutual_friends
    
    def create_post(self, title, content):
        """Créer un post"""
        db = get_db()
        post = Post(title=title, content=content)
        
        user_node = db.nodes.match("User", id=self.id).first()
        post_node = Node("Post", **post.to_dict())
        
        db.create(post_node)
        rel = Relationship(user_node, "CREATED", post_node)
        db.create(rel)
        
        return post
    
    def get_posts(self):
        """Récupérer les posts d'un utilisateur"""
        db = get_db()
        query = """
        MATCH (u:User {id: $user_id})-[:CREATED]->(p:Post)
        RETURN p
        """
        result = db.run(query, user_id=self.id).data()
        posts = []
        for record in result:
            post = Post()
            for key, value in record['p'].items():
                setattr(post, key, value)
            posts.append(post)
        return posts
    
    def like_post(self, post_id):
        """Aimer un post"""
        db = get_db()
        user_node = db.nodes.match("User", id=self.id).first()
        post_node = db.nodes.match("Post", id=post_id).first()
        
        if user_node and post_node:
            # Vérifier si l'utilisateur a déjà aimé le post
            query = """
            MATCH (u:User {id: $user_id})-[r:LIKES]->(p:Post {id: $post_id})
            RETURN r
            """
            result = db.run(query, user_id=self.id, post_id=post_id).data()
            
            if len(result) == 0:
                rel = Relationship(user_node, "LIKES", post_node)
                db.create(rel)
                return True
        return False
    
    def unlike_post(self, post_id):
        """Ne plus aimer un post"""
        db = get_db()
        query = """
        MATCH (u:User {id: $user_id})-[r:LIKES]->(p:Post {id: $post_id})
        DELETE r
        """
        db.run(query, user_id=self.id, post_id=post_id)
        return True
    
    def like_comment(self, comment_id):
        """Aimer un commentaire"""
        db = get_db()
        user_node = db.nodes.match("User", id=self.id).first()
        comment_node = db.nodes.match("Comment", id=comment_id).first()
        
        if user_node and comment_node:
            # Vérifier si l'utilisateur a déjà aimé le commentaire
            query = """
            MATCH (u:User {id: $user_id})-[r:LIKES]->(c:Comment {id: $comment_id})
            RETURN r
            """
            result = db.run(query, user_id=self.id, comment_id=comment_id).data()
            
            if len(result) == 0:
                rel = Relationship(user_node, "LIKES", comment_node)
                db.create(rel)
                return True
        return False
    
    def unlike_comment(self, comment_id):
        """Ne plus aimer un commentaire"""
        db = get_db()
        query = """
        MATCH (u:User {id: $user_id})-[r:LIKES]->(c:Comment {id: $comment_id})
        DELETE r
        """
        db.run(query, user_id=self.id, comment_id=comment_id)
        return True
    
    def create_comment(self, post_id, content):
        """Créer un commentaire"""
        db = get_db()
        comment = Comment(content=content)
        
        user_node = db.nodes.match("User", id=self.id).first()
        post_node = db.nodes.match("Post", id=post_id).first()
        comment_node = Node("Comment", **comment.to_dict())
        
        if user_node and post_node:
            db.create(comment_node)
            user_rel = Relationship(user_node, "CREATED", comment_node)
            post_rel = Relationship(post_node, "HAS_COMMENT", comment_node)
            db.create(user_rel)
            db.create(post_rel)
            return comment
        return None

class Post(BaseModel):
    """Modèle pour les posts"""
    
    def __init__(self, title=None, content=None):
        super().__init__()
        self.title = title
        self.content = content
    
    def get_creator(self):
        """Récupérer le créateur du post"""
        db = get_db()
        query = """
        MATCH (u:User)-[:CREATED]->(p:Post {id: $post_id})
        RETURN u
        """
        result = db.run(query, post_id=self.id).data()
        if result:
            creator = User()
            for key, value in result[0]['u'].items():
                setattr(creator, key, value)
            return creator
        return None
    
    def get_comments(self):
        """Récupérer les commentaires d'un post"""
        db = get_db()
        query = """
        MATCH (p:Post {id: $post_id})-[:HAS_COMMENT]->(c:Comment)
        RETURN c
        """
        result = db.run(query, post_id=self.id).data()
        comments = []
        for record in result:
            comment = Comment()
            for key, value in record['c'].items():
                setattr(comment, key, value)
            comments.append(comment)
        return comments
    
    def get_likes_count(self):
        """Récupérer le nombre de likes d'un post"""
        db = get_db()
        query = """
        MATCH (:User)-[:LIKES]->(p:Post {id: $post_id})
        RETURN count(*) AS likes_count
        """
        result = db.run(query, post_id=self.id).data()
        return result[0]['likes_count'] if result else 0

class Comment(BaseModel):
    """Modèle pour les commentaires"""
    
    def __init__(self, content=None):
        super().__init__()
        self.content = content
    
    def get_creator(self):
        """Récupérer le créateur du commentaire"""
        db = get_db()
        query = """
        MATCH (u:User)-[:CREATED]->(c:Comment {id: $comment_id})
        RETURN u
        """
        result = db.run(query, comment_id=self.id).data()
        if result:
            creator = User()
            for key, value in result[0]['u'].items():
                setattr(creator, key, value)
            return creator
        return None
    
    def get_post(self):
        """Récupérer le post auquel appartient le commentaire"""
        db = get_db()
        query = """
        MATCH (p:Post)-[:HAS_COMMENT]->(c:Comment {id: $comment_id})
        RETURN p
        """
        result = db.run(query, comment_id=self.id).data()
        if result:
            post = Post()
            for key, value in result[0]['p'].items():
                setattr(post, key, value)
            return post
        return None
    
    def get_likes_count(self):
        """Récupérer le nombre de likes d'un commentaire"""
        db = get_db()
        query = """
        MATCH (:User)-[:LIKES]->(c:Comment {id: $comment_id})
        RETURN count(*) AS likes_count
        """
        result = db.run(query, comment_id=self.id).data()
        return result[0]['likes_count'] if result else 0

# app/db_init.py
from app import create_app, db
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
import uuid
import time

def init_db():
    """Initialise la base de données avec des données de test"""
    print("Initialisation de la base de données avec des données de test...")
    
    # Réinitialiser la base de données
    query = """
    MATCH (n)
    DETACH DELETE n
    """
    db.run(query)
    print("Base de données réinitialisée.")
    
    # Créer des utilisateurs
    alice = User(name="Alice Martin", email="alice@example.com")
    bob = User(name="Bob Dupont", email="bob@example.com")
    charlie = User(name="Charlie Garcia", email="charlie@example.com")
    dave = User(name="Dave Johnson", email="dave@example.com")
    eve = User(name="Eve Wilson", email="eve@example.com")
    
    # Enregistrer les utilisateurs
    alice.save()
    bob.save()
    charlie.save()
    dave.save()
    eve.save()
    
    print(f"Utilisateurs créés: {alice.id}, {bob.id}, {charlie.id}, {dave.id}, {eve.id}")
    
    # Créer des relations d'amitié
    alice.add_friend(bob.id)
    alice.add_friend(charlie.id)
    bob.add_friend(dave.id)
    charlie.add_friend(eve.id)
    dave.add_friend(eve.id)
    bob.add_friend(charlie.id)  # Pour les amis en commun avec Alice
    
    print("Relations d'amitié créées.")
    
    # Créer des posts
    post1 = Post(
        title="Introduction à Neo4j", 
        content="Neo4j est une base de données orientée graphe très puissante pour modéliser des relations complexes.", 
        user_id=alice.id
    )
    post2 = Post(
        title="Flask et les APIs REST", 
        content="Flask est un micro-framework Python idéal pour créer des APIs RESTful rapidement.", 
        user_id=bob.id
    )
    post3 = Post(
        title="Les réseaux sociaux et les bases de données graphes", 
        content="Les bases de données graphes comme Neo4j sont parfaites pour implémenter les fonctionnalités d'un réseau social.", 
        user_id=charlie.id
    )
    
    # Enregistrer les posts
    post1.save()
    post2.save()
    post3.save()
    
    print(f"Posts créés: {post1.id}, {post2.id}, {post3.id}")
    
    # Créer des commentaires
    comment1 = Comment(
        content="Super article sur Neo4j ! J'ai beaucoup appris.", 
        user_id=bob.id, 
        post_id=post1.id
    )
    comment2 = Comment(
        content="J'utilise Flask depuis des années, c'est vraiment génial.", 
        user_id=alice.id, 
        post_id=post2.id
    )
    comment3 = Comment(
        content="Tu as parfaitement raison concernant Neo4j et les réseaux sociaux.", 
        user_id=eve.id, 
        post_id=post3.id
    )
    comment4 = Comment(
        content="As-tu des exemples concrets de cas d'utilisation ?", 
        user_id=dave.id, 
        post_id=post1.id
    )
    
    # Enregistrer les commentaires
    comment1.save()
    comment2.save()
    comment3.save()
    comment4.save()
    
    print(f"Commentaires créés: {comment1.id}, {comment2.id}, {comment3.id}, {comment4.id}")
    
    # Ajouter des likes aux posts
    post1.like(bob.id)
    post1.like(charlie.id)
    post1.like(dave.id)
    post2.like(alice.id)
    post2.like(charlie.id)
    post3.like(alice.id)
    post3.like(bob.id)
    post3.like(dave.id)
    post3.like(eve.id)
    
    print("Likes ajoutés aux posts.")
    
    # Ajouter des likes aux commentaires
    comment1.like(alice.id)
    comment1.like(charlie.id)
    comment2.like(bob.id)
    comment2.like(charlie.id)
    comment3.like(charlie.id)
    comment4.like(alice.id)
    comment4.like(charlie.id)
    
    print("Likes ajoutés aux commentaires.")
    
    print("Initialisation de la base de données terminée.")
    print("\nStatistiques :")
    print(f"- Utilisateurs : 5")
    print(f"- Posts : 3")
    print(f"- Commentaires : 4")
    print(f"- Relations d'amitié : 6")
    print(f"- Likes sur les posts : 9")
    print(f"- Likes sur les commentaires : 7")
    
    print("\nUtilisateurs créés :")
    for user in [alice, bob, charlie, dave, eve]:
        print(f"- {user.name} (ID: {user.id})")
    
    return {
        "users": {
            "alice": alice.id,
            "bob": bob.id,
            "charlie": charlie.id,
            "dave": dave.id,
            "eve": eve.id
        },
        "posts": {
            "neo4j_intro": post1.id,
            "flask_api": post2.id,
            "social_networks": post3.id
        },
        "comments": {
            "comment1": comment1.id,
            "comment2": comment2.id,
            "comment3": comment3.id,
            "comment4": comment4.id
        }
    }

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        init_db()

from flask import Blueprint, jsonify, request
from app.models.post import Post
from app.models.user import User

post_bp = Blueprint('post_bp', __name__)

@post_bp.route('', methods=['GET'])
def get_posts():
    """Route pour récupérer tous les posts"""
    try:
        posts = Post.find_all()
        return jsonify({
            'status': 'success',
            'posts': [post.to_dict() for post in posts]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@post_bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    """Route pour récupérer un post par son ID"""
    try:
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({
                'status': 'error',
                'message': f'Post avec l\'ID {post_id} non trouvé'
            }), 404
        
        # Récupérer le nombre de likes
        likes_count = post.get_likes_count()
        
        # Ajouter le nombre de likes au dictionnaire du post
        post_dict = post.to_dict()
        post_dict['likes_count'] = likes_count
        
        return jsonify({
            'status': 'success',
            'post': post_dict
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@post_bp.route('/<post_id>', methods=['PUT'])
def update_post(post_id):
    """Route pour mettre à jour un post"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Données JSON manquantes'
            }), 400
        
        # Vérifier que le post existe
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({
                'status': 'error',
                'message': f'Post avec l\'ID {post_id} non trouvé'
            }), 404
        
        # Mettre à jour les attributs du post
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
        
        # Enregistrer les modifications
        post.save()
        
        return jsonify({
            'status': 'success',
            'message': 'Post mis à jour avec succès',
            'post': post.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@post_bp.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Route pour supprimer un post"""
    try:
        # Vérifier que le post existe
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({
                'status': 'error',
                'message': f'Post avec l\'ID {post_id} non trouvé'
            }), 404
        
        # Supprimer le post
        Post.delete(post_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Post avec l\'ID {post_id} supprimé avec succès'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@post_bp.route('/<post_id>/like', methods=['POST'])
def like_post(post_id):
    """Route pour ajouter un like à un post"""
    try:
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'ID utilisateur manquant dans les données'
            }), 400
        
        user_id = data['user_id']
        
        # Vérifier que l'utilisateur et le post existent
        user = User.find_by_id(user_id)
        post = Post.find_by_id(post_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        if not post:
            return jsonify({
                'status': 'error',
                'message': f'Post avec l\'ID {post_id} non trouvé'
            }), 404
        
        # Ajouter le like
        post.like(user_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Like ajouté au post {post_id} par l\'utilisateur {user_id}'
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@post_bp.route('/<post_id>/like', methods=['DELETE'])
def unlike_post(post_id):
    """Route pour retirer un like d'un post"""
    try:
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'ID utilisateur manquant dans les données'
            }), 400
        
        user_id = data['user_id']
        
        # Vérifier que l'utilisateur et le post existent
        user = User.find_by_id(user_id)
        post = Post.find_by_id(post_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        if not post:
            return jsonify({
                'status': 'error',
                'message': f'Post avec l\'ID {post_id} non trouvé'
            }), 404
        
        # Retirer le like
        post.unlike(user_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Like retiré du post {post_id} par l\'utilisateur {user_id}'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Mettre ces routes ici plutôt que dans user_routes pour garder une logique cohérente
@post_bp.route('/users/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Route pour récupérer les posts d'un utilisateur"""
    try:
        # Vérifier que l'utilisateur existe
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        # Récupérer les posts de l'utilisateur
        posts = Post.find_by_user(user_id)
        
        return jsonify({
            'status': 'success',
            'posts': [post.to_dict() for post in posts]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@post_bp.route('/users/<user_id>/posts', methods=['POST'])
def create_post(user_id):
    """Route pour créer un post"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Données JSON manquantes'
            }), 400
        
        # Vérifier que les champs requis sont présents
        if 'title' not in data or 'content' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Les champs title et content sont requis'
            }), 400
        
        # Vérifier que l'utilisateur existe
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        # Créer et enregistrer le nouveau post
        post = Post(title=data['title'], content=data['content'], user_id=user_id)
        post.save()
        
        return jsonify({
            'status': 'success',
            'message': 'Post créé avec succès',
            'post': post.to_dict()
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

from flask import Blueprint, jsonify, request
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User

comment_bp = Blueprint('comment_bp', __name__)

@comment_bp.route('', methods=['GET'])
def get_comments():
    """Route pour récupérer tous les commentaires"""
    try:
        comments = Comment.find_all()
        return jsonify({
            'status': 'success',
            'comments': [comment.to_dict() for comment in comments]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@comment_bp.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    """Route pour récupérer un commentaire par son ID"""
    try:
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return jsonify({
                'status': 'error',
                'message': f'Commentaire avec l\'ID {comment_id} non trouvé'
            }), 404
        
        return jsonify({
            'status': 'success',
            'comment': comment.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@comment_bp.route('/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Route pour mettre à jour un commentaire"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Données JSON manquantes'
            }), 400
        
        # Vérifier que le commentaire existe
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return jsonify({
                'status': 'error',
                'message': f'Commentaire avec l\'ID {comment_id} non trouvé'
            }), 404
        
        # Mettre à jour le contenu du commentaire
        if 'content' in data:
            comment.content = data['content']
        
        # Enregistrer les modifications
        comment.save()
        
        return jsonify({
            'status': 'success',
            'message': 'Commentaire mis à jour avec succès',
            'comment': comment.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@comment_bp.route('/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Route pour supprimer un commentaire"""
    try:
        # Vérifier que le commentaire existe
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return jsonify({
                'status': 'error',
                'message': f'Commentaire avec l\'ID {comment_id} non trouvé'
            }), 404
        
        # Supprimer le commentaire
        Comment.delete(comment_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Commentaire avec l\'ID {comment_id} supprimé avec succès'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@comment_bp.route('/<comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    """Route pour ajouter un like à un commentaire"""
    try:
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'ID utilisateur manquant dans les données'
            }), 400
        
        user_id = data['user_id']
        
        # Vérifier que l'utilisateur et le commentaire existent
        user = User.find_by_id(user_id)
        comment = Comment.find_by_id(comment_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        if not comment:
            return jsonify({
                'status': 'error',
                'message': f'Commentaire avec l\'ID {comment_id} non trouvé'
            }), 404
        
        # Ajouter le like
        comment.like(user_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Like ajouté au commentaire {comment_id} par l\'utilisateur {user_id}'
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@comment_bp.route('/<comment_id>/like', methods=['DELETE'])
def unlike_comment(comment_id):
    """Route pour retirer un like d'un commentaire"""
    try:
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'ID utilisateur manquant dans les données'
            }), 400
        
        user_id = data['user_id']
        
        # Vérifier que l'utilisateur et le commentaire existent
        user = User.find_by_id(user_id)
        comment = Comment.find_by_id(comment_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        if not comment:
            return jsonify({
                'status': 'error',
                'message': f'Commentaire avec l\'ID {comment_id} non trouvé'
            }), 404
        
        # Retirer le like
        comment.unlike(user_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Like retiré du commentaire {comment_id} par l\'utilisateur {user_id}'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Routes pour les commentaires liés à un post
@comment_bp.route('/posts/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """Route pour récupérer les commentaires d'un post"""
    try:
        # Vérifier que le post existe
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({
                'status': 'error',
                'message': f'Post avec l\'ID {post_id} non trouvé'
            }), 404
        
        # Récupérer les commentaires du post
        comments = Comment.find_by_post(post_id)
        
        return jsonify({
            'status': 'success',
            'comments': [comment.to_dict() for comment in comments]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@comment_bp.route('/posts/<post_id>/comments', methods=['POST'])
def create_comment(post_id):
    """Route pour ajouter un commentaire à un post"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Données JSON manquantes'
            }), 400
        
        # Vérifier que les champs requis sont présents
        if 'content' not in data or 'user_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Les champs content et user_id sont requis'
            }), 400
        
        # Vérifier que l'utilisateur et le post existent
        user_id = data['user_id']
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
        
        # Créer et enregistrer le nouveau commentaire
        comment = Comment(content=data['content'], user_id=user_id, post_id=post_id)
        comment.save()
        
        return jsonify({
            'status': 'success',
            'message': 'Commentaire créé avec succès',
            'comment': comment.to_dict()
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@comment_bp.route('/posts/<post_id>/comments/<comment_id>', methods=['DELETE'])
def delete_post_comment(post_id, comment_id):
    """Route pour supprimer un commentaire d'un post"""
    try:
        # Vérifier que le post et le commentaire existent
        post = Post.find_by_id(post_id)
        comment = Comment.find_by_id(comment_id)
        
        if not post:
            return jsonify({
                'status': 'error',
                'message': f'Post avec l\'ID {post_id} non trouvé'
            }), 404
        
        if not comment:
            return jsonify({
                'status': 'error',
                'message': f'Commentaire avec l\'ID {comment_id} non trouvé'
            }), 404
        
        # Vérifier que le commentaire appartient bien au post
        if comment.post_id != post_id:
            return jsonify({
                'status': 'error',
                'message': f'Le commentaire {comment_id} n\'appartient pas au post {post_id}'
            }), 400
        
        # Supprimer le commentaire
        Comment.delete(comment_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Commentaire avec l\'ID {comment_id} supprimé avec succès du post {post_id}'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

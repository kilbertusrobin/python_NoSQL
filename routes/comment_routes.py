from flask import Blueprint, jsonify, request
from models import Comment, User

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/', methods=['GET'])
def get_comments():
    """R�cup�rer tous les commentaires"""
    comments = Comment.find_all()
    return jsonify([comment.to_dict() for comment in comments])

@comment_bp.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    """R�cup�rer un commentaire par son ID"""
    comment = Comment.find_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Commentaire non trouv�'}), 404
    return jsonify(comment.to_dict())

@comment_bp.route('/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Mettre � jour un commentaire"""
    comment = Comment.find_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Commentaire non trouv�'}), 404
    
    data = request.json
    if not data:
        return jsonify({'error': 'Aucune donn�e fournie'}), 400
    
    # Mettre � jour les champs fournis
    update_fields = {}
    if 'content' in data:
        update_fields['content'] = data['content']
    
    comment.update(**update_fields)
    return jsonify(comment.to_dict())

@comment_bp.route('/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Supprimer un commentaire"""
    comment = Comment.find_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Commentaire non trouv�'}), 404
    
    comment.delete()
    return jsonify({'message': 'Commentaire supprim� avec succ�s'})

@comment_bp.route('/<comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    """Ajouter un like � un commentaire"""
    comment = Comment.find_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Commentaire non trouv�'}), 404
    
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({'error': 'L\'ID de l\'utilisateur est requis'}), 400
    
    user_id = data['user_id']
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouv�'}), 404
    
    success = user.like_comment(comment_id)
    if success:
        return jsonify({'message': 'Commentaire aim� avec succ�s'})
    else:
        return jsonify({'message': 'L\'utilisateur a d�j� aim� ce commentaire'})

@comment_bp.route('/<comment_id>/like', methods=['DELETE'])
def unlike_comment(comment_id):
    """Retirer un like d'un commentaire"""
    comment = Comment.find_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Commentaire non trouv�'}), 404
    
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({'error': 'L\'ID de l\'utilisateur est requis'}), 400
    
    user_id = data['user_id']
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouv�'}), 404
    
    user.unlike_comment(comment_id)
    return jsonify({'message': 'Like retir� avec succ�s'})

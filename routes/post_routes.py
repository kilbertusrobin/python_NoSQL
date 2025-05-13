from flask import Blueprint, jsonify, request
from models import Post, User

post_bp = Blueprint('post', __name__)

@post_bp.route('/', methods=['GET'])
def get_posts():
    """Récupérer tous les posts"""
    posts = Post.find_all()
    return jsonify([post.to_dict() for post in posts])

@post_bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    """Récupérer un post par son ID"""
    post = Post.find_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post non trouvé'}), 404
    return jsonify(post.to_dict())

@post_bp.route('/<post_id>', methods=['PUT'])
def update_post(post_id):
    """Mettre à jour un post"""
    post = Post.find_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post non trouvé'}), 404
    
    data = request.json
    if not data:
        return jsonify({'error': 'Aucune donnée fournie'}), 400
    
    # Mettre à jour les champs fournis
    update_fields = {}
    if 'title' in data:
        update_fields['title'] = data['title']
    if 'content' in data:
        update_fields['content'] = data['content']
    
    post.update(**update_fields)
    return jsonify(post.to_dict())

@post_bp.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Supprimer un post"""
    post = Post.find_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post non trouvé'}), 404
    
    post.delete()
    return jsonify({'message': 'Post supprimé avec succès'})

@post_bp.route('/<post_id>/like', methods=['POST'])
def like_post(post_id):
    """Ajouter un like à un post"""
    post = Post.find_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post non trouvé'}), 404
    
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({'error': 'L\'ID de l\'utilisateur est requis'}), 400
    
    user_id = data['user_id']
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    success = user.like_post(post_id)
    if success:
        return jsonify({'message': 'Post aimé avec succès'})
    else:
        return jsonify({'message': 'L\'utilisateur a déjà aimé ce post'})

@post_bp.route('/<post_id>/like', methods=['DELETE'])
def unlike_post(post_id):
    """Retirer un like d'un post"""
    post = Post.find_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post non trouvé'}), 404
    
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({'error': 'L\'ID de l\'utilisateur est requis'}), 400
    
    user_id = data['user_id']
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    user.unlike_post(post_id)
    return jsonify({'message': 'Like retiré avec succès'})

@post_bp.route('/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """Récupérer les commentaires d'un post"""
    post = Post.find_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post non trouvé'}), 404
    
    comments = post.get_comments()
    return jsonify([comment.to_dict() for comment in comments])

@post_bp.route('/<post_id>/comments', methods=['POST'])
def create_comment(post_id):
    """Ajouter un commentaire à un post"""
    post = Post.find_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post non trouvé'}), 404
    
    data = request.json
    if not data or 'content' not in data or 'user_id' not in data:
        return jsonify({'error': 'Les champs content et user_id sont requis'}), 400
    
    user_id = data['user_id']
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    comment = user.create_comment(post_id=post_id, content=data['content'])
    if not comment:
        return jsonify({'error': 'Erreur lors de la création du commentaire'}), 500
    
    return jsonify(comment.to_dict()), 201

@post_bp.route('/<post_id>/comments/<comment_id>', methods=['DELETE'])
def delete_post_comment(post_id, comment_id):
    """Supprimer un commentaire d'un post"""
    from models import Comment
    
    post = Post.find_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post non trouvé'}), 404
    
    comment = Comment.find_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Commentaire non trouvé'}), 404
    
    # Vérifier que le commentaire appartient bien au post
    post_of_comment = comment.get_post()
    if not post_of_comment or post_of_comment.id != post_id:
        return jsonify({'error': 'Ce commentaire n\'appartient pas à ce post'}), 400
    
    comment.delete()
    return jsonify({'message': 'Commentaire supprimé avec succès'})

from flask import Blueprint, jsonify, request
from models import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    """Récupérer la liste des utilisateurs"""
    users = User.find_all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/', methods=['POST'])
def create_user():
    """Créer un nouvel utilisateur"""
    data = request.json
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Les champs name et email sont requis'}), 400
    
    user = User(name=data['name'], email=data['email'])
    user.save()
    return jsonify(user.to_dict()), 201

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Récupérer un utilisateur par son ID"""
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    return jsonify(user.to_dict())

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Mettre à jour un utilisateur par son ID"""
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    data = request.json
    if not data:
        return jsonify({'error': 'Aucune donnée fournie'}), 400
    
    # Mettre à jour les champs fournis
    update_fields = {}
    if 'name' in data:
        update_fields['name'] = data['name']
    if 'email' in data:
        update_fields['email'] = data['email']
    
    user.update(**update_fields)
    return jsonify(user.to_dict())

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Supprimer un utilisateur par son ID"""
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    user.delete()
    return jsonify({'message': 'Utilisateur supprimé avec succès'})

@user_bp.route('/<user_id>/friends', methods=['GET'])
def get_user_friends(user_id):
    """Récupérer la liste des amis d'un utilisateur"""
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    friends = user.get_friends()
    return jsonify([friend.to_dict() for friend in friends])

@user_bp.route('/<user_id>/friends', methods=['POST'])
def add_friend(user_id):
    """Ajouter un ami"""
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    data = request.json
    if not data or 'friend_id' not in data:
        return jsonify({'error': 'L\'ID de l\'ami est requis'}), 400
    
    friend_id = data['friend_id']
    friend = User.find_by_id(friend_id)
    if not friend:
        return jsonify({'error': 'Ami non trouvé'}), 404
    
    if user.id == friend_id:
        return jsonify({'error': 'Un utilisateur ne peut pas être ami avec lui-même'}), 400
    
    if user.is_friend_with(friend_id):
        return jsonify({'message': 'Ces utilisateurs sont déjà amis'})
    
    user.add_friend(friend_id)
    return jsonify({'message': 'Ami ajouté avec succès'})

@user_bp.route('/<user_id>/friends/<friend_id>', methods=['DELETE'])
def remove_friend(user_id, friend_id):
    """Supprimer un ami"""
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    friend = User.find_by_id(friend_id)
    if not friend:
        return jsonify({'error': 'Ami non trouvé'}), 404
    
    if not user.is_friend_with(friend_id):
        return jsonify({'error': 'Ces utilisateurs ne sont pas amis'}), 400
    
    user.remove_friend(friend_id)
    return jsonify({'message': 'Ami supprimé avec succès'})

@user_bp.route('/<user_id>/friends/<friend_id>', methods=['GET'])
def check_friendship(user_id, friend_id):
    """Vérifier si deux utilisateurs sont amis"""
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    friend = User.find_by_id(friend_id)
    if not friend:
        return jsonify({'error': 'Ami non trouvé'}), 404
    
    is_friend = user.is_friend_with(friend_id)
    return jsonify({'are_friends': is_friend})

@user_bp.route('/<user_id>/mutual-friends/<other_id>', methods=['GET'])
def get_mutual_friends(user_id, other_id):
    """Récupérer les amis en commun"""
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    other_user = User.find_by_id(other_id)
    if not other_user:
        return jsonify({'error': 'Autre utilisateur non trouvé'}), 404
    
    mutual_friends = user.get_mutual_friends(other_id)
    return jsonify([friend.to_dict() for friend in mutual_friends])

@user_bp.route('/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Récupérer les posts d'un utilisateur"""
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    posts = user.get_posts()
    return jsonify([post.to_dict() for post in posts])

@user_bp.route('/<user_id>/posts', methods=['POST'])
def create_user_post(user_id):
    """Créer un post"""
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    data = request.json
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Les champs title et content sont requis'}), 400
    
    post = user.create_post(title=data['title'], content=data['content'])
    return jsonify(post.to_dict()), 201

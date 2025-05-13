from flask import Blueprint, jsonify, request
from app.models.user import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('', methods=['GET'])
def get_users():
    """Route pour récupérer la liste des utilisateurs"""
    try:
        users = User.find_all()
        return jsonify({
            'status': 'success',
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@user_bp.route('', methods=['POST'])
def create_user():
    """Route pour créer un nouvel utilisateur"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Données JSON manquantes'
            }), 400
        
        # Vérifier que les champs requis sont présents
        if 'name' not in data or 'email' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Les champs name et email sont requis'
            }), 400
        
        # Créer et enregistrer le nouvel utilisateur
        user = User(name=data['name'], email=data['email'])
        user.save()
        
        return jsonify({
            'status': 'success',
            'message': 'Utilisateur créé avec succès',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Route pour récupérer un utilisateur par son ID"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        return jsonify({
            'status': 'success',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Route pour mettre à jour un utilisateur par son ID"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Données JSON manquantes'
            }), 400
        
        # Vérifier que l'utilisateur existe
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        # Mettre à jour les attributs de l'utilisateur
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        
        # Enregistrer les modifications
        user.save()
        
        return jsonify({
            'status': 'success',
            'message': 'Utilisateur mis à jour avec succès',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Route pour supprimer un utilisateur par son ID"""
    try:
        # Vérifier que l'utilisateur existe
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        # Supprimer l'utilisateur
        User.delete(user_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Utilisateur avec l\'ID {user_id} supprimé avec succès'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@user_bp.route('/<user_id>/friends', methods=['GET'])
def get_friends(user_id):
    """Route pour récupérer la liste des amis d'un utilisateur"""
    try:
        # Vérifier que l'utilisateur existe
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        # Récupérer les amis
        friends = user.get_friends()
        
        return jsonify({
            'status': 'success',
            'friends': [friend.to_dict() for friend in friends]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@user_bp.route('/<user_id>/friends', methods=['POST'])
def add_friend(user_id):
    """Route pour ajouter un ami (ID de l'ami dans le body)"""
    try:
        data = request.get_json()
        if not data or 'friend_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'ID de l\'ami manquant dans les données'
            }), 400
        
        friend_id = data['friend_id']
        
        # Vérifier que les deux utilisateurs existent
        user = User.find_by_id(user_id)
        friend = User.find_by_id(friend_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        if not friend:
            return jsonify({
                'status': 'error',
                'message': f'Ami avec l\'ID {friend_id} non trouvé'
            }), 404
        
        # Vérifier qu'un utilisateur ne peut pas s'ajouter lui-même
        if user_id == friend_id:
            return jsonify({
                'status': 'error',
                'message': 'Un utilisateur ne peut pas s\'ajouter lui-même comme ami'
            }), 400
        
        # Ajouter l'ami
        user.add_friend(friend_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Amitié créée entre les utilisateurs {user_id} et {friend_id}'
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@user_bp.route('/<user_id>/friends/<friend_id>', methods=['DELETE'])
def remove_friend(user_id, friend_id):
    """Route pour supprimer un ami"""
    try:
        # Vérifier que les deux utilisateurs existent
        user = User.find_by_id(user_id)
        friend = User.find_by_id(friend_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        if not friend:
            return jsonify({
                'status': 'error',
                'message': f'Ami avec l\'ID {friend_id} non trouvé'
            }), 404
        
        # Supprimer l'amitié
        user.remove_friend(friend_id)
        
        return jsonify({
            'status': 'success',
            'message': f'Amitié supprimée entre les utilisateurs {user_id} et {friend_id}'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@user_bp.route('/<user_id>/friends/<friend_id>', methods=['GET'])
def check_friendship(user_id, friend_id):
    """Route pour vérifier si deux utilisateurs sont amis"""
    try:
        # Vérifier que les deux utilisateurs existent
        user = User.find_by_id(user_id)
        friend = User.find_by_id(friend_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        if not friend:
            return jsonify({
                'status': 'error',
                'message': f'Ami avec l\'ID {friend_id} non trouvé'
            }), 404
        
        # Vérifier l'amitié
        are_friends = User.check_friendship(user_id, friend_id)
        
        return jsonify({
            'status': 'success',
            'are_friends': are_friends
        }), 200 except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@user_bp.route('/<user_id>/mutual-friends/<other_id>', methods=['GET'])
def get_mutual_friends(user_id, other_id):
    """Route pour récupérer les amis en commun"""
    try:
        # Vérifier que les deux utilisateurs existent
        user = User.find_by_id(user_id)
        other = User.find_by_id(other_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {user_id} non trouvé'
            }), 404
        
        if not other:
            return jsonify({
                'status': 'error',
                'message': f'Utilisateur avec l\'ID {other_id} non trouvé'
            }), 404
        
        # Récupérer les amis en commun
        mutual_friends = User.get_mutual_friends(user_id, other_id)
        
        return jsonify({
            'status': 'success',
            'mutual_friends': [friend.to_dict() for friend in mutual_friends]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

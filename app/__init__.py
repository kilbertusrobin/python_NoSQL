from flask import Flask
from flask_cors import CORS
from .config import Config
from .database import Database

# Initialiser la connexion à la base de données
db = Database().get_db()

def create_app(config_class=Config):
    # Initialiser l'application Flask
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Activer CORS pour permettre les requêtes cross-origin
    CORS(app)
    
    # Enregistrer les blueprints pour les routes
    from .routes.user_routes import user_bp
    from .routes.post_routes import post_bp
    from .routes.comment_routes import comment_bp
    
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(comment_bp, url_prefix='/comments')
    
    @app.route('/')
    def index():
        return {
            'message': 'Bienvenue sur l\'API Neo4j Social Network',
            'status': 'API en ligne',
            'endpoints': {
                'users': '/users',
                'posts': '/posts',
                'comments': '/comments'
            }
        }
    
    return app

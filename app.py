from flask import Flask, jsonify, request
from database import get_db
import models
import routes

app = Flask(__name__)

# Initialiser la base de données
@app.before_first_request
def init_db():
    db = get_db()
    # Créer des contraintes pour assurer l'unicité
    db.run("CREATE CONSTRAINT IF NOT EXISTS ON (u:User) ASSERT u.id IS UNIQUE")
    db.run("CREATE CONSTRAINT IF NOT EXISTS ON (p:Post) ASSERT p.id IS UNIQUE")
    db.run("CREATE CONSTRAINT IF NOT EXISTS ON (c:Comment) ASSERT c.id IS UNIQUE")

# Enregistrer les blueprints
app.register_blueprint(routes.user_bp, url_prefix='/users')
app.register_blueprint(routes.post_bp, url_prefix='/posts')
app.register_blueprint(routes.comment_bp, url_prefix='/comments')

@app.route('/')
def index():
    return jsonify({'message': 'Bienvenue sur l\'API Flask Neo4j'})

if __name__ == '__main__':
    app.run(debug=True)

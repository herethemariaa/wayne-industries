from flask import Flask, session
from flask_cors import CORS
from database import init_db
from auth import auth_bp
from resources import resources_bp

app = Flask(__name__)
app.secret_key = 'chave_secreta'

# Configuração do CORS para permitir requisições do frontend
CORS(app, supports_credentials=True)

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(resources_bp, url_prefix='/api')

# Inicializar o banco de dados

if __name__ == "__main__":
    with app.app_context():
        init_db()
    print("Banco inicializado com sucesso!")
    app.run(debug=True)